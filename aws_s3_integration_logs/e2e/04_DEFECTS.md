# E2E defects and blockers — 2026-11-16

## Resolved blocker E2E-001 — isolated runtime startup

- Resolved by building `aws-bank-e2e:latest` from the existing Linux wheels and running it with isolated temporary paths and the Floci network only.

## E2E-002 — promotion does not require a passing candidate evaluation

- `POST /api/admin/train` created version 2.
- `POST /api/admin/models/2/promote` returned success before a completed evaluation for version 2.
- `POST /api/admin/evals/run?version=2` then returned `quality_gate.passed=false` (recall 0.4286 vs minimum 0.5).
- This violates the requested “promotion activates only an approved model” acceptance condition. No implementation change was made during this validation task.

## E2E-003 — rollback blocked after failed gate evidence

- A rollback attempt using `POST /api/admin/models/1/promote` returned HTTP 409 because the persisted failed quality gate blocked promotion.
- This leaves rollback-to-previous-approved-model unverified and requires product/governance decision before remediation.

## Unresolved validation risks

- Candidate promotion gating and rollback behavior require remediation/approval before GO.
- Existing artifact-suite evidence in the repository records 19 passed and 1 skipped; the reported 20/20 result was not independently rerun during this validation pass.
- No credentials, customer data, real AWS resources, or production endpoints were used.
