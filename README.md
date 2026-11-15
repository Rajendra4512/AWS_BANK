# AWS_BANK — lightweight fraud MLOps operations platform

**Status: runnable MVP foundation, not a production banking platform.** Real scoring, candidate training, model promotion/rollback, PSI drift simulation, admin/user authentication, editable lessons, and audit events are implemented. Synthetic data only. Optional MLflow tracking is provided but not installed in the 1 GB base image. Evidently and Bedrock are documented extension points, **not implemented integrations**.

## Quick start (Windows PowerShell)

1. Create folder `AWS_BANK`, extract ZIP contents into it, and open PowerShell there.
2. `Copy-Item .env.example .env`
3. Edit `.env`: set a unique admin password of at least 12 characters; generate a session secret with `python -c "import secrets; print(secrets.token_hex(32))"`.
4. `docker compose up --build -d` (only this Compose project; **never** use global prune/down commands).
5. Open http://localhost:7005 and sign in as `admin` using your chosen password.
6. Admin → Model Registry → Train candidate → Promote. Then score transactions, run drift checks, and explore Learning Lab.
7. `docker compose logs --tail=100 aws-bank` to inspect logs. `docker compose down` stops only this project; volumes are bind-mounted and preserved.

## Security caveats

Localhost-only binding. No default passwords, no public sign-up, server-side RBAC, HTTP-only session cookies. Before AWS/public deployment implement HTTPS and secure cookies, CSRF protection, rate limiting, account lockout, MFA, secret rotation, artifact signature validation, data encryption, immutable audit, backups, vulnerability scans, and independent model validation. Joblib artifacts must never be supplied by untrusted users. Never expose port 7005 publicly without an authenticated TLS proxy.

## Resource management

1 GB container, 1.5 CPU, single worker, BLAS threads capped, no Redis, no frontend build server, no separate database process. Training is synchronous and short; for production use job queues. Optional MLflow adds substantial memory and may require raising container memory or using remote tracking. No Kaggle dataset is bundled because of licensing, privacy and size; synthetic data allows offline start.

## Engineering documents

Read `docs/00_INDEX.md` for BRD, PRD, architecture, solution design, engineering design, stories, runbook, AWS plan, acceptance matrix and learning syllabus.

## Expanded banking AI modules (v1)
- **Credit Risk:** `/api/credit/assess` implements a transparent heuristic index, not a calibrated PD model.
- **AML:** `/api/aml/screen` creates persistent cases; `/api/cases` lists; `/api/cases/{id}/review` enforces distinct requester/reviewer.
- **LLMOps:** `/api/llm/query` is an offline curated knowledge gateway; `/api/admin/evals/run` persists deterministic keyword checks.
- **Admin:** `/api/admin/providers` manages provider metadata but deliberately blocks enabling external inference without an adapter.
- **Learning Lab:** new domain-specific lessons are editable by administrators; docs/12–17 provide interview study notes.

**Scope truth:** These are executable educational baselines, not production-grade banking models or an AWS deployment. MLflow tracking is optional and its native registry is not yet integrated. Evidently, Bedrock, LangGraph, production-grade credit PD and AML anomaly models remain tracked implementation items in `docs/20_BACKLOG.md`.

Run `powershell -ExecutionPolicy Bypass -File scripts/verify.ps1` from the project directory after setting `.env`. Never expose port 7005 to the internet before completing security release gates.
