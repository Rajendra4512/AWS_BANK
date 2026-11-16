"""Versioned model artifact storage with local and opt-in S3 backends.

S3 model objects are untrusted input: joblib deserialization can execute code.
Only use a bucket/prefix controlled by the deployment and never load artifacts
from an untrusted S3 location.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path

import joblib


class ArtifactStoreError(RuntimeError):
    """Fail-closed storage or integrity error."""


class ArtifactExistsError(ArtifactStoreError):
    """A model version already has an artifact or manifest."""


class ArtifactStore:
    """Store immutable versioned model artifacts locally or in S3-compatible storage."""

    def __init__(self, root, *, backend=None, bucket=None, prefix=None, region=None, endpoint_url=None):
        self.root = Path(root)
        self.backend = (backend or os.getenv("AWS_BANK_ARTIFACT_BACKEND", "local")).lower()
        if self.backend not in {"local", "s3"}:
            raise ArtifactStoreError("AWS_BANK_ARTIFACT_BACKEND must be local or s3")
        self.bucket = bucket or os.getenv("AWS_BANK_S3_BUCKET", "")
        self.prefix = (prefix if prefix is not None else os.getenv("AWS_BANK_S3_PREFIX", "models")).strip("/")
        self.region = region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        self.endpoint_url = endpoint_url if endpoint_url is not None else os.getenv("AWS_ENDPOINT_URL")
        self._s3 = None
        if self.backend == "local":
            self.root.mkdir(parents=True, exist_ok=True)
        elif not self.bucket:
            raise ArtifactStoreError("AWS_BANK_S3_BUCKET is required for the s3 backend")

    def _client(self):
        if self._s3 is None:
            try:
                import boto3
                from botocore.config import Config
            except ImportError as exc:
                raise ArtifactStoreError("boto3 is required for the s3 artifact backend") from exc
            self._s3 = boto3.client("s3", region_name=self.region, endpoint_url=self.endpoint_url, config=Config(connect_timeout=5, read_timeout=30, retries={"max_attempts": 3, "mode": "standard"}))
        return self._s3

    def path(self, version):
        if self.backend == "local":
            return self.root / f"model_v{version}.joblib"
        return f"s3://{self.bucket}/{self._key(version)}"

    def _key(self, version):
        name = f"model_v{version}.joblib"
        return f"{self.prefix}/{name}" if self.prefix else name

    def _manifest_key(self, version):
        name = f"model_v{version}.sha256.json"
        return f"{self.prefix}/{name}" if self.prefix else name

    def _local_manifest_path(self, version):
        return self.root / f"model_v{version}.sha256.json"

    @staticmethod
    def _manifest_bytes(version, digest, provenance=None):
        manifest = {"version": version, "sha256": digest}
        if provenance is not None:
            manifest["provenance"] = provenance
        return json.dumps(manifest, sort_keys=True).encode("utf-8")

    @staticmethod
    def _serialize(model):
        stream = io.BytesIO()
        joblib.dump(model, stream)
        data = stream.getvalue()
        return data, hashlib.sha256(data).hexdigest()

    @staticmethod
    def _is_missing(exc):
        code = str(getattr(exc, "response", {}).get("Error", {}).get("Code", ""))
        return code in {"404", "NoSuchKey", "NotFound"}

    @staticmethod
    def _write_exclusive(path, data, label):
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
            fd = os.open(path, flags, 0o600)
        except FileExistsError as exc:
            raise ArtifactExistsError(f"{label} already exists") from exc
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
        except Exception as exc:
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass
            raise ArtifactStoreError(f"{label} write failed") from exc

    def save(self, model, version):
        data, digest = self._serialize(model)
        if self.backend == "local":
            target = self.path(version)
            manifest_path = self._local_manifest_path(version)
            if target.exists() or manifest_path.exists():
                raise ArtifactExistsError(f"Artifact version {version} already exists")
            self._write_exclusive(target, data, f"Artifact version {version}")
            manifest = self._manifest_bytes(version, digest)
            self._write_exclusive(manifest_path, manifest, f"Artifact manifest version {version}")
            return target

        client = self._client()
        key, manifest_key = self._key(version), self._manifest_key(version)
        for candidate, label in ((key, "artifact"), (manifest_key, "manifest")):
            try:
                client.head_object(Bucket=self.bucket, Key=candidate)
                raise ArtifactExistsError(f"Artifact {label} version {version} already exists")
            except ArtifactExistsError:
                raise
            except Exception as exc:
                if not self._is_missing(exc):
                    raise ArtifactStoreError(f"Unable to verify S3 {label} immutability") from exc
        manifest = self._manifest_bytes(version, digest)
        try:
            client.put_object(Bucket=self.bucket, Key=key, Body=data, ContentType="application/octet-stream", Metadata={"sha256": digest}, IfNoneMatch="*")
            client.put_object(Bucket=self.bucket, Key=manifest_key, Body=manifest, ContentType="application/json", IfNoneMatch="*")
        except Exception as exc:
            code = str(getattr(exc, "response", {}).get("Error", {}).get("Code", ""))
            if code in {"409", "412", "PreconditionFailed"}:
                raise ArtifactExistsError(f"Artifact version {version} already exists") from exc
            raise ArtifactStoreError("S3 artifact upload failed; no local fallback was attempted") from exc
        return self.path(version)

    def inspect(self, version):
        """Return publication state without modifying either backend."""
        if self.backend == "local":
            artifact = self.path(version).exists()
            manifest = self._local_manifest_path(version).exists()
        else:
            client = self._client()
            present = []
            for key, label in ((self._key(version), "artifact"), (self._manifest_key(version), "manifest")):
                try:
                    client.head_object(Bucket=self.bucket, Key=key)
                except Exception as exc:
                    if self._is_missing(exc):
                        present.append(False)
                        continue
                    raise ArtifactStoreError(f"Unable to inspect S3 {label} version {version}") from exc
                present.append(True)
            artifact, manifest = present
        if artifact and manifest:
            state = "published"
        elif artifact or manifest:
            state = "incomplete"
        else:
            state = "missing"
        return {"version": version, "artifact": artifact, "manifest": manifest, "state": state}

    def reconcile_incomplete(self, version, *, expected_sha256=None, approve=False):
        """Publish only a verified missing manifest; never overwrite or delete.

        ``expected_sha256`` must come from the writer's trusted publication
        record. This method does not infer ownership of an orphaned object.
        """
        if not approve:
            raise ArtifactStoreError("Explicit approval is required for incomplete artifact reconciliation")
        state = self.inspect(version)
        if state["state"] != "incomplete":
            raise ArtifactStoreError(f"Artifact version {version} is not incomplete")
        if not state["artifact"]:
            raise ArtifactStoreError(f"Artifact version {version} has no model bytes to reconcile")
        if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
            raise ArtifactStoreError("A verified expected_sha256 is required for reconciliation")
        try:
            if self.backend == "local":
                data = self.path(version).read_bytes()
            else:
                data = self._client().get_object(Bucket=self.bucket, Key=self._key(version))["Body"].read()
        except Exception as exc:
            raise ArtifactStoreError(f"Artifact version {version} could not be read for reconciliation") from exc
        if hashlib.sha256(data).hexdigest() != expected_sha256:
            raise ArtifactStoreError(f"Artifact version {version} reconciliation checksum mismatch")
        manifest = self._manifest_bytes(version, expected_sha256, "approved-reconciliation")
        if self.backend == "local":
            self._write_exclusive(self._local_manifest_path(version), manifest, f"Artifact manifest version {version}")
            return self._local_manifest_path(version)
        try:
            self._client().put_object(
                Bucket=self.bucket,
                Key=self._manifest_key(version),
                Body=manifest,
                ContentType="application/json",
                IfNoneMatch="*",
            )
        except Exception as exc:
            code = str(getattr(exc, "response", {}).get("Error", {}).get("Code", ""))
            if code in {"409", "412", "PreconditionFailed"}:
                raise ArtifactExistsError(f"Artifact manifest version {version} already exists") from exc
            raise ArtifactStoreError("S3 manifest reconciliation failed") from exc
        return self.path(version)

    def _download_verified(self, version, client=None):
        client = client or self._client()
        try:
            body = client.get_object(Bucket=self.bucket, Key=self._key(version))["Body"].read()
            manifest_bytes = client.get_object(Bucket=self.bucket, Key=self._manifest_key(version))["Body"].read()
        except Exception as exc:
            if self._is_missing(exc):
                raise ArtifactStoreError(f"Artifact version {version} is missing") from exc
            raise ArtifactStoreError("S3 artifact download failed") from exc
        try:
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError, TypeError) as exc:
            raise ArtifactStoreError(f"Artifact version {version} manifest is malformed") from exc
        actual = hashlib.sha256(body).hexdigest()
        if manifest.get("version") != version or manifest.get("sha256") != actual:
            raise ArtifactStoreError(f"Artifact version {version} checksum mismatch")
        return body

    def exists(self, version):
        if self.backend == "local":
            try:
                self._local_download_verified(version)
                return True
            except ArtifactStoreError as exc:
                if str(exc) == f"Artifact version {version} is missing":
                    return False
                raise
        try:
            self._download_verified(version)
            return True
        except ArtifactStoreError as exc:
            if str(exc) == f"Artifact version {version} is missing":
                return False
            raise

    def load(self, version):
        if self.backend == "local":
            return joblib.load(io.BytesIO(self._local_download_verified(version)))
        return joblib.load(io.BytesIO(self._download_verified(version)))

    def migrate_legacy_local(self, version, backup_dir, *, approve=False, verified_provenance=None, validated_sha256=None):
        """Migrate one trusted manifest-less local artifact after explicit approval.

        The source is copied exclusively to a separate backup directory before
        validation. This method never deserializes legacy bytes. A separately
        isolated validator must provide trusted provenance and the validated
        SHA-256 before this method can publish a manifest.
        """
        if self.backend != "local":
            raise ArtifactStoreError("Legacy migration is supported only by the local backend")
        if not approve:
            raise ArtifactStoreError("Explicit approval is required for legacy artifact migration")
        if not isinstance(verified_provenance, str) or not verified_provenance.strip():
            raise ArtifactStoreError("Verified provenance is required for legacy artifact migration")
        if not isinstance(validated_sha256, str) or len(validated_sha256) != 64:
            raise ArtifactStoreError("An isolated validation SHA-256 is required for legacy artifact migration")
        source = self.path(version)
        manifest_path = self._local_manifest_path(version)
        if not source.exists():
            raise ArtifactStoreError(f"Legacy artifact version {version} is missing")
        if manifest_path.exists():
            raise ArtifactExistsError(f"Artifact version {version} already has a manifest")
        backup_root = Path(backup_dir)
        if backup_root.resolve() == self.root.resolve():
            raise ArtifactStoreError("Legacy backup directory must be separate from the artifact directory")
        backup_root.mkdir(parents=True, exist_ok=True)
        source_bytes = source.read_bytes()
        backup_path = backup_root / source.name
        self._write_exclusive(backup_path, source_bytes, f"Legacy backup version {version}")
        digest = hashlib.sha256(source_bytes).hexdigest()
        if digest != validated_sha256:
            raise ArtifactStoreError(f"Legacy artifact version {version} failed isolated validation")
        current_bytes = source.read_bytes()
        if current_bytes != source_bytes:
            raise ArtifactStoreError(f"Legacy artifact version {version} changed during migration")
        manifest = self._manifest_bytes(version, digest, verified_provenance.strip())
        self._write_exclusive(manifest_path, manifest, f"Artifact manifest version {version}")
        return manifest_path

    def _local_download_verified(self, version):
        try:
            body = self.path(version).read_bytes()
            manifest_bytes = self._local_manifest_path(version).read_bytes()
        except FileNotFoundError as exc:
            raise ArtifactStoreError(f"Artifact version {version} is missing") from exc
        try:
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError, TypeError) as exc:
            raise ArtifactStoreError(f"Artifact version {version} manifest is malformed") from exc
        actual = hashlib.sha256(body).hexdigest()
        if manifest.get("version") != version or manifest.get("sha256") != actual:
            raise ArtifactStoreError(f"Artifact version {version} checksum mismatch")
        return body
