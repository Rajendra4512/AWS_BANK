# CI failure root causes — 2026-11-16

## Root cause 1: stale admin test ordering

`tests/test_domains.py::test_banking_workflows` called `/api/admin/cloud-readiness` before logging in. The endpoint correctly returned HTTP 401. The test was inconsistent with the application’s admin guard.

## Root cause 2: stale evaluation expectation

The same test called evaluation before any model was promoted. The application correctly returned `ml_model_eval.status == "not_run"` and did not fabricate held-out ML cases; the test incorrectly required at least 600 executed cases.

## Root cause 3: CI offline Docker context

`Dockerfile` requires `COPY wheels/ /srv/wheels/`, but `.gitignore` excludes `wheels/` and `git ls-files wheels` is empty. A GitHub checkout therefore has no wheelhouse and the offline Docker build fails unless CI generates it first.

## Remote evidence limitation

Actual GitHub failure logs were not retrievable because the installed GitHub CLI is unauthenticated. Causes above are reproduced locally in an equivalent Linux environment with actual failure output.
