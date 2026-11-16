# Governance remediation test results — 2026-11-16

## Static and unit evidence

- `python -m py_compile app/main.py tests/test_model_governance.py`: PASS.
- The image initially lacked pytest. A disposable run installed only `pytest==8.3.5` and `httpx==0.28.1` into ephemeral `/tmp/testdeps`; no host/global installation occurred.
- Final `python -m pytest tests/test_model_governance.py -v`: PASS — 6 passed, 0 failed, 0 skipped, exit code 0. Warnings were FastAPI deprecation and read-only pytest-cache warnings.

## API regression counts

- PASS: 11 checks/workflows in the final isolated API sequence, plus 6 focused pytest tests.
- FAIL: 0 after remediation.
- SKIP: 0.
- BLOCKED: 0.

Final internal API regression run: stale-threshold promotion HTTP 409; exact-version mismatch promotion HTTP 409; current exact-version passing promotion HTTP 200; active version 2; rejected audit count 2.

Evidence included:

- anonymous promotion `401`; admin login `200`;
- passing candidate evaluation and promotion `200`;
- failed evaluation followed by promotion denial `409`, active model remained version 1;
- passing version 2 evaluation and promotion `200`;
- candidate without evaluation denied `409`;
- never-approved rollback denied `409`;
- approved rollback restored version 1 `200`;
- corrupted rollback manifest denied `409`, active version remained 1;
- inference after rollback returned `200` using version 1;
- audit contained successful and rejected governance actions, with 4 rejected records.
