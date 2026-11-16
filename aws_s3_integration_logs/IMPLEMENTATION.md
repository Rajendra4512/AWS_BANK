# Floci S3 artifact storage implementation — 2026-11-16

- `app/artifacts.py` now preserves local mode as the default and supports opt-in `AWS_BANK_ARTIFACT_BACKEND=s3`.
- Configuration: `AWS_BANK_ARTIFACT_BACKEND`, `AWS_BANK_S3_BUCKET`, `AWS_BANK_S3_PREFIX`, `AWS_REGION`, and `AWS_ENDPOINT_URL`.
- S3 uses lazy boto3 initialization with 5-second connect timeout, 30-second read timeout and three standard retries.
- Uploads serialize bytes once, calculate SHA-256, store an independent versioned manifest, use conditional writes, and reject existing versions.
- Downloads require the manifest, verify version and SHA-256, and fail closed on missing objects, storage errors or mismatches. No local fallback exists in S3 mode.
- Local mode preserves `path`, `save`, `exists` and `load` behavior while using exclusive creation to prevent overwrites.
- `main.py` training, promotion and inference and `domains.py` evaluation continue to construct `ArtifactStore` from the same environment-driven backend configuration.
- No DB schema, promotion contract, quality gate, audit behavior or rollback logic was changed.
- Security boundary: joblib deserialization can execute code; only load artifacts from a trusted controlled bucket/prefix.
- Legacy compatibility: manifest-less local artifacts are rejected by normal `load()`; `migrate_legacy_local(version, backup_dir, approve=True)` is the explicit migration procedure. It makes an exclusive backup, validates the trusted legacy bytes, confirms the source did not change, and writes an exclusive SHA-256 manifest. Failed validation leaves the backup and does not publish a manifest.
- Recovery boundary: incomplete publication is never silently repaired or deleted. Orphaned artifact bytes remain unusable until a separately approved recovery decision; existing writer-owned backups/objects are never overwritten.
