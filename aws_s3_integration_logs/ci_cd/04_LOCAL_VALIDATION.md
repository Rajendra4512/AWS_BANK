# Local CI-equivalent validation — 2026-11-16

## Equivalent Linux test command

- Disposable `aws-bank-e2e:latest` container, repository mounted read-only, ephemeral `/tmp` dependencies, and ephemeral app data/artifact paths.
- Installed only temporary test tools `pytest==8.3.5` and `httpx==0.28.1` inside the disposable container.
- Command: `AWS_BANK_DATA_DIR=/tmp/data AWS_BANK_ARTIFACT_DIR=/tmp/artifacts PYTHONPATH=/tmp/testdeps:/workspace python -m pytest -q tests`
- Result: **34 passed, 1 skipped**, exit code 0.
- The skipped test is the opt-in live-Floci test.

## Other gates

- `python -m compileall -q app`: PASS.
- `pwsh -NoProfile -File scripts/security_scan.ps1`: PASS — no high-risk embedded credential patterns.
- `docker compose -p aws_bank_ci config --quiet` with CI dummy bootstrap/session values: PASS.
- `docker build --pull=false --tag aws-bank-ci-check:local .`: PASS using the existing local Linux wheelhouse.
- `git check-ignore -v wheels` and `git ls-files wheels`: confirmed generated wheelhouse is ignored and untracked; the workflow now creates it on CI.
- No secrets, real credentials, customer data, or generated test artifacts were added to tracked source.
