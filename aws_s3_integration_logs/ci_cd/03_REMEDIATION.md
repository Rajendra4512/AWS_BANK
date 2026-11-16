# CI remediation — 2026-11-16

- `tests/test_domains.py`: moved the cloud-readiness assertion after authenticated admin login while preserving the unauthenticated access check.
- `tests/test_domains.py`: changed the no-active-model evaluation assertion to require `ml_model_eval.status == "not_run"` and at least the 13 non-ML evaluation cases, preserving fail-closed no-fabrication behavior.
- `.github/workflows/ci.yml`: added `python -m pip download --only-binary=:all: --dest wheels -r requirements.txt` immediately before the offline Docker build. This creates the ignored Linux wheelhouse in CI without committing generated wheels or changing application dependencies.
- No application business logic, S3 integration, governance logic, database schema, Dockerfile, compose contract, or existing container was changed.
