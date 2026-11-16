# E2E scenarios — 2026-11-16

| Scenario | Result | Evidence |
|---|---|---|
| Training creates S3 model and SHA-256 manifest | PASS | `POST /api/admin/train` returned candidate versions 1 and 2; Floci prefix contained both `.joblib` and `.sha256.json` objects. Independent digest comparison matched. |
| Evaluation computes real metrics and governance gate | PASS | `POST /api/admin/evals/run?version=2` returned completed metrics for 600 synthetic samples; gate returned `passed:false` with recall 0.4286 below 0.5. |
| Promotion activates approved model only | FAIL | Version 2 was promoted before its version-specific evaluation; later failed evaluation did not prevent the earlier promotion. |
| Inference loads active model from Floci S3 | PASS | `/api/score` returned model versions 1 and 2 with real probabilities; local artifact file count was 0. |
| Rollback restores approved model | BLOCKED | Promotion of version 1 as rollback returned 409 because persisted failed quality-gate evidence blocked it. |
| Audit records capture lifecycle actions | PASS | `/api/admin/audit` returned lifecycle actions including `model.train` and `model.promote_or_rollback`. |
| Missing/corrupt artifacts fail closed | PASS | Corrupted and then removed active manifest caused `/api/score` HTTP 500; no prediction was returned. |
| Local/S3 backends do not fall back | PASS | Isolated S3 app had zero local artifact files; storage failure surfaced as HTTP 500. |
| Role-based administrative access | PASS | Unauthenticated train returned 401; authenticated non-admin train returned 403; admin training succeeded. |
| `main.py` ArtifactStore consistency | PASS — static plus runtime | Training, promotion and score constructed `ArtifactStore(ART)` with S3 environment configuration. |
| `domains.py` ArtifactStore consistency | PASS — static inspection only | `active_model_eval` constructs `ArtifactStore` from `AWS_BANK_ARTIFACT_DIR`; backend remains environment-driven. |
