# E2E execution results — 2026-11-16

## Commands and actual results

- `git status --short --branch`: PASS; branch and existing changes verified.
- `docker ps --format ...`: PASS read-only inventory; existing Floci and application containers remained running.
- Temporary-context `docker build --pull=false --tag aws-bank-e2e:latest ...`: PASS; all pinned requirements resolved from the existing Linux wheel inventory.
- Disposable `aws-bank-e2e` startup: PASS after UID/GID-owned tmpfs correction; `/api/health` returned HTTP 200.
- Dedicated Floci bucket creation through the disposable app runtime: PASS; no real AWS resource used.
- `Invoke-WebRequest http://127.0.0.1:4566/health`: PASS, HTTP 200.
- `Invoke-WebRequest http://127.0.0.1:7005/health`: 404; no lifecycle request was sent to the existing application.
- `POST /api/login`, user creation/login, anonymous admin train and non-admin admin train: PASS; responses were 200/401/403 as expected.
- Training, evaluation, promotion, inference, audit and corruption/missing-manifest API calls: executed; detailed scenario status is in `02_TEST_SCENARIOS.md`.

## Counts

- PASS: 11 checks/workflows, including build, startup, RBAC, training, S3 publication, evaluation execution, inference, audit, integrity failure handling and no-fallback behavior.
- FAIL: 1 — promotion allowed version 2 before a completed passing version-specific evaluation.
- SKIP: 0 explicit scenario skips.
- BLOCKED: 1 — rollback to version 1 was refused by the persisted failed quality gate.

No API workflow was claimed as passed without execution.
