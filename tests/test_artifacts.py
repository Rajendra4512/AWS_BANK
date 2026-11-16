import hashlib
import io
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor

import joblib
import pytest
from botocore.exceptions import ClientError

from app.artifacts import ArtifactExistsError, ArtifactStore, ArtifactStoreError


class _Body:
    def __init__(self, value):
        self.value = value

    def read(self):
        return self.value


class FakeS3:
    def __init__(self):
        self.objects = {}
        self.fail_put = False
        self.fail_put_keys = set()
        self.permission_keys = set()
        self._lock = threading.Lock()

    @staticmethod
    def missing(key):
        return ClientError({"Error": {"Code": "NoSuchKey", "Message": "missing"}}, "GetObject")

    def head_object(self, *, Bucket, Key):
        if Key in self.permission_keys:
            raise ClientError({"Error": {"Code": "AccessDenied", "Message": "denied"}}, "HeadObject")
        if (Bucket, Key) not in self.objects:
            raise self.missing(Key)
        return {"ContentLength": len(self.objects[(Bucket, Key)])}

    def put_object(self, *, Bucket, Key, Body, **kwargs):
        if Key in self.permission_keys:
            raise ClientError({"Error": {"Code": "AccessDenied", "Message": "denied"}}, "PutObject")
        if self.fail_put or Key in self.fail_put_keys:
            raise ClientError({"Error": {"Code": "503", "Message": "synthetic failure"}}, "PutObject")
        with self._lock:
            if kwargs.get("IfNoneMatch") == "*" and (Bucket, Key) in self.objects:
                raise ClientError({"Error": {"Code": "412", "Message": "already exists"}}, "PutObject")
            self.objects[(Bucket, Key)] = Body if isinstance(Body, bytes) else Body.read()
        return {"ETag": '"synthetic"'}

    def get_object(self, *, Bucket, Key):
        if Key in self.permission_keys:
            raise ClientError({"Error": {"Code": "AccessDenied", "Message": "denied"}}, "GetObject")
        if (Bucket, Key) not in self.objects:
            raise self.missing(Key)
        return {"Body": _Body(self.objects[(Bucket, Key)])}


def _store(tmp_path, fake):
    store = ArtifactStore(
        tmp_path,
        backend="s3",
        bucket="floci-test-bucket",
        prefix="synthetic/models",
        region="us-east-1",
        endpoint_url="http://127.0.0.1:9000",
    )
    store._s3 = fake
    return store


def test_local_backend_preserves_path_save_load_exists(tmp_path):
    model = {"kind": "local-compatible"}
    store = ArtifactStore(tmp_path, backend="local")
    path = store.save(model, 1)
    assert path == tmp_path / "model_v1.joblib"
    assert store.exists(1)
    assert store.load(1) == model
    with pytest.raises(ArtifactExistsError):
        store.save(model, 1)


def test_local_interrupted_write_cannot_be_loaded(tmp_path, monkeypatch):
    store = ArtifactStore(tmp_path, backend="local")
    original = os.fdopen

    def interrupted(fd, *args, **kwargs):
        handle = original(fd, *args, **kwargs)
        original_write = handle.write

        def fail(value):
            original_write(value[:4])
            raise OSError("synthetic interrupted write")

        handle.write = fail
        return handle

    monkeypatch.setattr(os, "fdopen", interrupted)
    with pytest.raises(ArtifactStoreError, match="write failed"):
        store.save({"kind": "interrupted"}, 5)
    assert not store.path(5).exists()
    with pytest.raises(ArtifactStoreError, match="missing"):
        store.load(5)


def test_local_checksum_mismatch_fails_before_deserialization(tmp_path):
    store = ArtifactStore(tmp_path, backend="local")
    store.save({"kind": "local-integrity"}, 12)
    store.path(12).write_bytes(b"corrupted")
    with pytest.raises(ArtifactStoreError, match="checksum mismatch"):
        store.load(12)


def test_legacy_local_artifact_requires_approved_migration(tmp_path):
    store = ArtifactStore(tmp_path, backend="local")
    legacy = {"kind": "legacy-trusted"}
    store.path(13).write_bytes(_joblib_bytes(legacy))
    with pytest.raises(ArtifactStoreError, match="Explicit approval"):
        store.migrate_legacy_local(13, tmp_path / "backups")
    with pytest.raises(ArtifactStoreError, match="missing"):
        store.load(13)
    digest = hashlib.sha256(store.path(13).read_bytes()).hexdigest()
    with pytest.raises(ArtifactStoreError, match="Verified provenance"):
        store.migrate_legacy_local(13, tmp_path / "backups", approve=True, validated_sha256=digest)
    manifest = store.migrate_legacy_local(
        13,
        tmp_path / "backups",
        approve=True,
        verified_provenance="synthetic trusted-local validation",
        validated_sha256=digest,
    )
    assert manifest.exists()
    assert (tmp_path / "backups" / "model_v13.joblib").read_bytes() == store.path(13).read_bytes()
    assert store.load(13) == legacy


def test_legacy_migration_does_not_deserialize_in_migration(tmp_path, monkeypatch):
    store = ArtifactStore(tmp_path, backend="local")
    source = store.path(16)
    source.write_bytes(_joblib_bytes({"kind": "legacy-isolated"}))
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    monkeypatch.setattr(joblib, "load", lambda *_args, **_kwargs: pytest.fail("migration deserialized bytes"))
    store.migrate_legacy_local(
        16,
        tmp_path / "backups",
        approve=True,
        verified_provenance="isolated synthetic validator",
        validated_sha256=digest,
    )


def test_legacy_migration_rejects_corrupt_bytes_and_preserves_backup(tmp_path):
    store = ArtifactStore(tmp_path, backend="local")
    source = store.path(14)
    source.write_bytes(b"not-a-joblib-model")
    backup_dir = tmp_path / "backups"
    with pytest.raises(ArtifactStoreError, match="failed isolated validation"):
        store.migrate_legacy_local(
            14,
            backup_dir,
            approve=True,
            verified_provenance="isolated synthetic validator",
            validated_sha256="0" * 64,
        )
    assert (backup_dir / "model_v14.joblib").read_bytes() == source.read_bytes()
    assert not store._local_manifest_path(14).exists()


def test_legacy_migration_never_overwrites_existing_backup(tmp_path):
    store = ArtifactStore(tmp_path, backend="local")
    legacy = {"kind": "legacy-backup"}
    store.path(15).write_bytes(_joblib_bytes(legacy))
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    existing = backup_dir / "model_v15.joblib"
    existing.write_bytes(b"other-writer-backup")
    with pytest.raises(ArtifactExistsError):
        store.migrate_legacy_local(
            15,
            backup_dir,
            approve=True,
            verified_provenance="isolated synthetic validator",
            validated_sha256=hashlib.sha256(store.path(15).read_bytes()).hexdigest(),
        )
    assert existing.read_bytes() == b"other-writer-backup"


def test_local_incomplete_publication_is_detected_and_reconciled(tmp_path):
    store = ArtifactStore(tmp_path, backend="local")
    data = _joblib_bytes({"kind": "local-incomplete"})
    store.path(17).write_bytes(data)
    assert store.inspect(17)["state"] == "incomplete"
    with pytest.raises(ArtifactStoreError, match="Explicit approval"):
        store.reconcile_incomplete(17, expected_sha256=hashlib.sha256(data).hexdigest())
    store.reconcile_incomplete(17, expected_sha256=hashlib.sha256(data).hexdigest(), approve=True)
    assert store.load(17) == {"kind": "local-incomplete"}


def _joblib_bytes(value):
    stream = io.BytesIO()
    joblib.dump(value, stream)
    return stream.getvalue()


def test_s3_round_trip_uses_manifest_and_floci_endpoint(tmp_path, monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "dummy-access")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "dummy-secret")
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://127.0.0.1:9000")
    fake = FakeS3()
    store = _store(tmp_path, fake)
    model = {"kind": "s3-round-trip"}
    assert store.save(model, 7) == "s3://floci-test-bucket/synthetic/models/model_v7.joblib"
    digest_key = ("floci-test-bucket", "synthetic/models/model_v7.sha256.json")
    manifest = json.loads(fake.objects[digest_key].decode())
    assert manifest["sha256"] == hashlib.sha256(fake.objects[("floci-test-bucket", "synthetic/models/model_v7.joblib")]).hexdigest()
    assert store.exists(7)
    assert store.load(7) == model


def test_s3_missing_object_fails_closed(tmp_path):
    store = _store(tmp_path, FakeS3())
    assert store.exists(99) is False
    with pytest.raises(ArtifactStoreError, match="missing"):
        store.load(99)


def test_s3_checksum_mismatch_fails_closed(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)
    store.save({"kind": "integrity"}, 2)
    manifest_key = ("floci-test-bucket", "synthetic/models/model_v2.sha256.json")
    manifest = json.loads(fake.objects[manifest_key].decode())
    manifest["sha256"] = "0" * 64
    fake.objects[manifest_key] = json.dumps(manifest).encode()
    with pytest.raises(ArtifactStoreError, match="checksum mismatch"):
        store.load(2)


def test_s3_manifest_upload_failure_leaves_unusable_artifact(tmp_path):
    fake = FakeS3()
    fake.fail_put_keys.add("synthetic/models/model_v6.sha256.json")
    store = _store(tmp_path, fake)
    with pytest.raises(ArtifactStoreError, match="no local fallback"):
        store.save({"kind": "manifest-failure"}, 6)
    assert ("floci-test-bucket", "synthetic/models/model_v6.joblib") in fake.objects
    assert store.exists(6) is False
    with pytest.raises(ArtifactStoreError, match="missing"):
        store.load(6)
    assert store.inspect(6)["state"] == "incomplete"
    artifact = fake.objects[("floci-test-bucket", "synthetic/models/model_v6.joblib")]
    digest = hashlib.sha256(artifact).hexdigest()
    fake.fail_put_keys.remove("synthetic/models/model_v6.sha256.json")
    store.reconcile_incomplete(6, expected_sha256=digest, approve=True)
    assert store.load(6) == {"kind": "manifest-failure"}


def test_s3_reconciliation_never_overwrites_manifest_from_other_writer(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)
    store.save({"kind": "reconcile-race"}, 18)
    manifest_key = ("floci-test-bucket", "synthetic/models/model_v18.sha256.json")
    artifact_key = ("floci-test-bucket", "synthetic/models/model_v18.joblib")
    del fake.objects[manifest_key]
    other_manifest = b'{"version":18,"sha256":"' + b"0" * 64 + b'"}'
    fake.objects[manifest_key] = other_manifest
    with pytest.raises(ArtifactStoreError, match="not incomplete"):
        store.reconcile_incomplete(18, expected_sha256=hashlib.sha256(fake.objects[artifact_key]).hexdigest(), approve=True)
    assert fake.objects[manifest_key] == other_manifest


def test_s3_missing_manifest_fails_closed(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)
    store.save({"kind": "missing-manifest"}, 8)
    del fake.objects[("floci-test-bucket", "synthetic/models/model_v8.sha256.json")]
    assert store.exists(8) is False
    with pytest.raises(ArtifactStoreError, match="missing"):
        store.load(8)


def test_s3_malformed_manifest_fails_closed(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)
    store.save({"kind": "malformed-manifest"}, 9)
    fake.objects[("floci-test-bucket", "synthetic/models/model_v9.sha256.json")] = b"not-json"
    with pytest.raises(ArtifactStoreError, match="manifest is malformed"):
        store.load(9)


def test_s3_permission_failure_fails_closed(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)
    store.save({"kind": "permission"}, 10)
    fake.permission_keys.add("synthetic/models/model_v10.joblib")
    with pytest.raises(ArtifactStoreError, match="download failed"):
        store.load(10)


def test_s3_failed_upload_does_not_fallback_local(tmp_path):
    fake = FakeS3()
    fake.fail_put = True
    store = _store(tmp_path, fake)
    with pytest.raises(ArtifactStoreError, match="no local fallback"):
        store.save({"kind": "failed-upload"}, 3)
    assert not list(tmp_path.glob("model_v3*"))


def test_s3_version_is_immutable(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)
    store.save({"kind": "first"}, 4)
    with pytest.raises(ArtifactExistsError):
        store.save({"kind": "second"}, 4)
    assert store.load(4) == {"kind": "first"}


def test_s3_conditional_write_allows_one_concurrent_writer(tmp_path):
    fake = FakeS3()
    store = _store(tmp_path, fake)

    def write(model):
        try:
            store.save(model, 11)
            return "saved"
        except ArtifactExistsError:
            return "exists"

    models = [{"kind": "writer-a"}, {"kind": "writer-b"}]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(write, models))
    assert sorted(results) == ["exists", "saved"]
    assert store.load(11) in models


@pytest.mark.skipif(os.getenv("AWS_BANK_RUN_FLOCI") != "1", reason="opt-in live Floci endpoint test")
def test_floci_live_round_trip(tmp_path):
    store = ArtifactStore(tmp_path, backend="s3")
    version = int(os.getenv("AWS_BANK_FLOCI_TEST_VERSION", "9001"))
    store.save({"kind": "live-floci"}, version)
    assert store.load(version) == {"kind": "live-floci"}
