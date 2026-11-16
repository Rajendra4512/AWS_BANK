# Governance remediation root cause — 2026-11-16

## Promotion defect

`app/main.py::promote()` previously checked artifact existence and only rejected an evaluation explicitly marked failed. It did not require a completed evaluation for the exact candidate version, did not reject missing/stale/mismatched evaluation evidence, and did not compare recorded thresholds with current governance settings. Therefore a candidate could become active without passing evaluation.

## Rollback defect

Rollback was not a distinct operation. The same `/api/admin/models/{version}/promote` endpoint handled both promotion and rollback, with no verifiable approval-history requirement. Existing `model.promote_or_rollback` audit entries were ambiguous and could not safely prove prior approval.

## Safe design decision

The existing `audit` table is sufficient without a schema change when successful candidate approval is recorded with the unambiguous `model.promote` action. The new rollback endpoint accepts only active/archived models with matching `model.promote` history. Legacy ambiguous actions are not treated as approval evidence; missing history fails closed.
