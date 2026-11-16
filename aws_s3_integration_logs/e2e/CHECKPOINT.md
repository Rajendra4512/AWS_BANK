# E2E checkpoint — 2026-11-16

- Preflight complete; no existing container or source directory was modified.
- Floci health check passed at `127.0.0.1:4566`.
- Isolated image built offline from pinned Linux wheels; app ran on only the Floci network with a fresh in-container database and unique prefix.
- API lifecycle executed through training, evaluation, promotion, inference, audit, RBAC and integrity-failure scenarios.
- Decision: NO-GO because promotion did not require a passing candidate evaluation and rollback was blocked by failed-gate evidence.
- Resume after approved governance remediation, then rerun with a fresh DB and unique Floci prefix.
