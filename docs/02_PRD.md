# Product requirements document (PRD)

## Personas and permissions
User: authenticate, score a synthetic transaction, inspect registry/drift history, read lessons. Admin: all user capabilities plus train, promote/rollback, run drift simulation, provision accounts, reset passwords via API, edit lessons and threshold, inspect audit. Future roles: model author, independent validator, approver, auditor.

## Functional requirements
FR-01 Login/logout with server-side sessions, no public signup. FR-02 Admin provisions a named user and role. FR-03 Admin resets passwords and invalidates sessions. FR-04 Admin trains deterministic synthetic-data classifier and stores versioned artifact and metrics. FR-05 Candidate is inactive until admin promotes. FR-06 Scoring always uses the active model and returns version, probability, threshold and advisory flag. FR-07 Admin runs drift simulation with configurable intensity and PSI threshold. FR-08 All users view drift history. FR-09 Admin promotes archived model to roll back. FR-10 Learning Lab lessons are editable by admin and readable by users. FR-11 Admin sees audit trail. FR-12 Health endpoint for probes.

## UX requirements
Clear left-to-right flow; visible model state; distinct candidate/active/archived statuses; validation errors shown; buttons must call real APIs. No simulated success banners. Learning text must distinguish actual implementation from proposed extensions.

## Nonfunctional requirements
Single container, localhost 7005, ≤1 GB configured memory, CPU-only, no always-running workers, persistent bind mounts, repeatable seed, testable APIs, 1-second typical scoring target on local laptop (benchmark, not guaranteed). Production targets: TLS, centralized identity, high availability, external database, observability, backup, and governance controls.

## Acceptance definition
No feature marked complete without a working backend route, UI action (where applicable), access test, failure path, and audit evidence for privileged changes. No claims of AWS, Evidently or managed MLflow integration until end-to-end verified.
