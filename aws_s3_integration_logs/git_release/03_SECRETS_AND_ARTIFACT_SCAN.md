# Secrets and artifact scan — 2026-11-16

- Bounded `rg` scan found no AWS access-key patterns, private-key blocks, session-token assignments, or GitHub token patterns outside excluded dependency/cache paths.
- `.env.example` contains placeholders only; no real credentials were staged.
- No `.joblib`, `.pkl`, `.sqlite`, `.sqlite3`, `.db`, `.bin`, or `.pyc` files were found in the release scope.
- No non-wheel files larger than 5 MiB were found in the release scope.
- `wheel-verification/` remains untracked and excluded; `wheels/` remains ignored/generated for offline Docker builds.
- Security workflow scan passed: no high-risk embedded credential patterns.
