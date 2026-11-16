# Floci S3 artifact storage test results — 2026-11-16

## PASS

- `python -m py_compile app/artifacts.py app/main.py app/domains.py`: PASS.
- `python -m py_compile app/artifacts.py`: PASS.
- `python -m pytest tests/test_artifacts.py -v`: BLOCKED at collection in the system Python because `joblib` is unavailable; no packages were installed.
- Final focused run used the existing offline dependency target via `PYTHONPATH=<host-temp-deps>;.`: PASS — 19 passed, 1 opt-in live-Floci test skipped in 0.84s.
- Coverage in `tests/test_artifacts.py`: local compatibility, approved legacy migration with provenance and no migration-time deserialization, approval refusal, corrupt legacy rejection with backup preservation, backup immutability, interrupted local write, local checksum mismatch, local incomplete recovery, fake-S3 round trip, missing object, missing/malformed manifest, checksum mismatch, permission failure, failed manifest upload and recovery, reconciliation immutability, failed upload with no fallback, version immutability, concurrent conditional writes with distinct writers, and an opt-in live-Floci round trip.
- `docker compose -p floci_artifact_test config --quiet` with process-local dummy bootstrap/session credentials: PASS. No container was started.

## BLOCKED / NOT RUN

- Live Floci endpoint round trip: NOT RUN; no Floci service was started and no network/cloud resource was provisioned.
- Full application training/evaluation/inference integration tests: NOT RUN because the Windows host lacks compatible application dependencies; Docker execution was explicitly prohibited. Existing `main.py` and `domains.py` ArtifactStore call sites were preserved and reviewed, but no unexecuted result is claimed.
- Full `tests/` suite: NOT RUN for the same host dependency limitation.

No passing result is claimed for blocked or unrun checks.
