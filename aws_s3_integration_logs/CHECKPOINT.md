# Floci S3 integration checkpoint — 2026-11-16

- Stage: implementation and isolated unit verification complete; live Floci integration remains pending.
- Modified implementation files: `app/artifacts.py`, `compose.yaml`, `.env.example`, `tests/test_artifacts.py`, `aws_s3_integration_logs/`.
- Preserved pre-existing user changes: `requirements.txt`, `wheel-verification/`.
- Not modified: original `AWS_BANK` directory, Docker resources, DB schema, `app/main.py`, `app/domains.py`, Dockerfile, existing tests.
- Current test evidence: final focused artifact tests PASS (19 passed, 1 opt-in live-Floci test skipped in 0.84s) using the existing offline dependency target. The exact bare command was blocked at collection because system Python lacks `joblib`; no packages were installed. Compose config PASS with dummy process-local credentials.
- Remaining gates: run the opt-in Floci S3 test with dummy credentials and `AWS_ENDPOINT_URL` after a Floci endpoint is made available, then run application training/evaluation/inference integration tests in an approved compatible environment.
- Approved design: legacy local model files without manifests are migrated only through explicit `migrate_legacy_local(..., approve=True, verified_provenance=..., validated_sha256=...)` with exclusive backup, externally isolated validation evidence, source-stability check and exclusive manifest publication. Migration never deserializes legacy bytes; normal `load()` continues to reject unverified legacy bytes.
- Recovery design: `inspect()` detects incomplete publication; `reconcile_incomplete(..., approve=True, expected_sha256=...)` can publish only a missing manifest after digest verification, with no overwrite or deletion.
- Resume rule: inspect `git status --short --branch` and this checkpoint before any next action. Do not push, merge or deploy without approval.
