# Engineering design

## Code map
`app/main.py`: schema, authentication, user management, training, registry, inference, PSI, lessons, audit. `app/index.html`: accessible minimal console and admin editor. `tests/test_smoke.py`: data shape, PSI identity, password verification. `compose.yaml`: constrained local runtime. `infra/`: AWS deployment guidance.

## Database entities
users(username PK, password PBKDF2, role, active); sessions(token_hash PK, username, expires); models(version PK, metrics JSON, status, source, created); predictions(version, features, score, ts); drift(psi, flag, details, ts); lessons(slug PK, title, content, updated); settings(key PK, value); audit(ts, actor, action, detail). SQLite for local single-instance only.

## HTTP API contract
- POST `/api/login`, `/api/logout`; GET `/api/me`, `/api/health`.
- GET `/api/models`; POST `/api/admin/train`; POST `/api/admin/models/{version}/promote`.
- POST `/api/score`; GET `/api/drift`; POST `/api/admin/drift-check?shift=0.8`.
- GET `/api/lessons`; PUT `/api/admin/lessons/{slug}`.
- GET/POST `/api/admin/users`; PUT `/api/admin/users/{username}/password`.
- GET `/api/admin/audit`, `/api/admin/settings`; PUT `/api/admin/settings/drift_threshold`.
FastAPI automatically exposes `/docs` for API exploration; auth required for protected routes.

## Failure behavior
No active model → 409; invalid credentials → 401; unauthorized role → 403; duplicate user → 409; invalid field → 422; missing artifact → 404; simultaneous training → 409. User-visible errors must not leak secrets.

## Threat model and production blockers
CSRF mitigation not implemented; cookie auth and mutating endpoints must not be internet-exposed. Rate limiting/lockout, MFA, secure cookies behind TLS, trusted proxies, CORS policy, audit immutability, storage encryption, artifact integrity, SAST, SCA, signed builds, backup restore, account deactivation and self-service password change are outstanding. Default admin password intentionally absent. Bootstrap credentials must come from `.env` or secret manager. A secure cookie should be enabled under HTTPS.

## Performance plan
One uvicorn worker, BLAS threads=1, bounded synthetic dataset, no always-on MLflow server. Measure RSS and CPU at startup, training, scoring and drift checks. Use task memory metrics and explicit alarms before AWS cutover.
