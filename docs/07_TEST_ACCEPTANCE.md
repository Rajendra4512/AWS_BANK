# Test and acceptance strategy

## Unit
`pytest -q tests/`: synthetic feature shape, identity PSI, password verification. Expand with PSI shift thresholds, invalid inputs, registry transitions, session expiry and metrics invariants.

## Integration (required before public deployment)
Start service with isolated temporary data and artifacts. Login admin; create user; verify user cannot POST admin endpoints; train candidate; confirm scoring fails before promotion; promote; score; simulate drift; create second version; roll back to first; confirm active version; edit lesson; reset user password; confirm old session invalidated; inspect audit. Capture request/response redacted logs.

## Security
CSRF, login brute force, session fixation/expiry, cross-role access, path injection, malicious serialized artifact, sensitive logging, secret scanning, dependency scan, Docker isolation and backup recovery. A 1 GB memory limit must be tested at training peak; no assertion of passing without measurement.

## Exit criteria
P0 APIs pass unit + integration + negative authorization; browser UI clicks verified; no secret committed; no critical vulnerabilities; reproducible container build; resource ceiling measured; clear operator rollback; production security controls implemented before AWS exposure.

## Current evidence
Scaffold includes unit tests but no claim of full E2E, load, cloud or security acceptance. Agent must execute tests and record actual outputs in `logs/`.
