# Isolated Floci E2E results — 2026-11-16

- Built `aws-bank-e2e:latest` with `docker build --pull=false` from the existing Dockerfile, pinned requirements, and existing Linux wheel inventory.
- Ran a disposable app on private `127.0.0.1:7009`, only on `aws-bank-floci_default`, with UID/GID-owned temporary `/srv/data` and `/srv/artifacts`, 1 GiB memory, 1.5 CPU, 128 PIDs, no-new-privileges, and all capabilities dropped.
- Used fresh in-container SQLite database, dummy credentials, synthetic banking data, dedicated local Floci bucket `aws-bank-e2e-governance-final`, and unique prefix `aws-bank-governance-20261116-final`.
- Existing `aws-bank-app` was not restarted or modified.
- Actual API sequence: train version 1; configure test-only thresholds `min_recall=0.4`, `max_false_positive_rate=0.5`; evaluate and promote version 1; train version 2; tighten threshold to `0.5`; evaluate version 2 and deny promotion; restore test threshold; evaluate/promote version 2; train version 3 and deny promotion without evaluation; deny rollback of never-approved version 3; rollback version 1; score version 1; corrupt version 2 manifest and deny rollback.
- Version 1 evaluation: HTTP 200, gate true, recall 0.4286 under explicitly configured 0.4 threshold.
- Version 2 failed evaluation: HTTP 200, gate false; promotion HTTP 409 and active remained version 1.
- Version 2 passing evaluation after explicit threshold configuration: HTTP 200, gate true; promotion HTTP 200, active version 2.
- Rollback version 1: HTTP 200, active version 1; inference HTTP 200 with model version 1.
- Corrupted version 2 rollback: HTTP 409; active version remained 1.
- API audit actions included `model.promote`, `model.rollback`, `model.promotion_rejected`, and `model.rollback_rejected`.
- Final internal API regression run: stale-threshold promotion HTTP 409; exact-version mismatch promotion HTTP 409; current exact-version passing promotion HTTP 200; active version 2; rejected audit count 2.
