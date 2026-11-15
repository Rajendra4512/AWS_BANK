# Compound engineering delivery contract

1. Baseline inventory: inspect exact files and docker compose resources; never prune, stop or restart unrelated containers.
2. Trace dependency graph with available Archify/Graphify tools where installed; if absent use targeted code search. Do not invent tool outputs.
3. Create branch `feature/aws-bank-hardening` before modifications; commit baseline and preserve rollback.
4. Prioritize missing functional integrations over UI changes. Each module: story → acceptance criteria → API/schema → implementation → tests → evidence → lesson tied to real code.
5. Before changes record CPU/RAM, current services, port 7005 ownership, test baseline and image hashes.
6. Implement minimal targeted changes. No unrelated refactors, destructive Docker commands, or touching other apps.
7. Execute focused tests, API security checks, browser journeys, memory profile, docker restart and persistence checks.
8. Store run logs under `logs/YYYYMMDD/` with command, outcome, failures, evidence and remediation.
9. Report exact status: implemented, partial, provisioned, blocked, or untested. Never claim AWS deployment from a local Docker smoke test.
10. Release only when gates in `18_RELEASE_GATES.md` pass; otherwise issue NO-GO with specific blockers.
