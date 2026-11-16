# Governance remediation implementation — 2026-11-16

- Changed `app/main.py` only for application behavior.
- Promotion now requires a verified artifact/manifest, candidate status, an exact-version completed evaluation newer than model creation, current threshold values, and `quality_gate.passed == true`.
- Missing, stale, mismatched, incomplete, failed, or threshold-stale evaluations are rejected before active-model updates.
- Rejected promotion and rollback actions are audited without changing the active model.
- Added distinct `POST /api/admin/models/{version}/rollback`.
- Rollback requires administrative authorization, verified artifact integrity, active/archived status, and an unambiguous prior `model.promote` audit record. Candidate, revoked/quarantined/unknown, corrupted, or historically unverified targets fail closed.
- Successful actions audit as `model.promote` and `model.rollback`; rejections audit as `model.promotion_rejected` and `model.rollback_rejected`.
- No database schema, S3 storage code, training, inference, RBAC, or unrelated application code was changed.
- Added focused regression tests in `tests/test_model_governance.py`.
