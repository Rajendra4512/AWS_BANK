# AI agent execution contract

## Scope and compound engineering
Read BRD → PRD → Architecture → Solution Design → Engineering Design → Stories → tests before changes. Map every requested feature to a story and acceptance test. Keep an implementation matrix: implemented, partial, planned, blocked. Preserve working behavior. Do not claim success without logs.

## Efficiency
Search file names, symbols and imports before opening full files. Limit reading to relevant code. Reuse modules. Prefer narrow edits and targeted tests. Optional Archify/Graphify tools: use only if installed, inspect permissions, and save diagrams under `docs/`; never block execution on missing plugins. Use UI consistency review rather than aesthetic-only rewrites.

## Docker safety — mandatory
Only operate on AWS_BANK Compose project. Before actions inspect `docker ps` and `docker compose config`. Never run `docker system prune`, `docker volume prune`, `docker network prune`, `docker rm -f` against unrelated containers, global stop, or `docker compose down -v`. Do not modify other projects, Docker daemon config, global networks or volumes. Keep localhost 7005 only; if occupied, report and ask before choosing another port. Set memory cap 1g, one worker, thread caps and bounded batch size. Never mount Docker socket or use privileged containers. Avoid image rebuilds unless source/dependency changed.

## Credentials and data
Never commit `.env`, API keys, AWS secrets, customer banking data or logs with PII. Bootstrap credentials must be supplied locally. Use synthetic transactions until explicit data license/privacy review. Do not make unapproved AWS changes or incur cloud charges.

## Implementation order
1. Check environment and files. 2. Build isolated container. 3. Run unit tests. 4. Verify login and RBAC. 5. Train/promote/score. 6. Drift simulation. 7. Rollback. 8. Learning admin edit. 9. Audit and resource benchmark. 10. Report evidence and blockers. Only after P0 acceptance consider P1 MLflow/Evidently and cloud.

## Logging
Create timestamped run directory under `logs/YYYYMMDD_HHMM/`; write preflight.md, changes.md, tests.md, resources.md, security.md, go_no_go.md. Redact credentials. Summarize modified files, test commands, results and unresolved risks. Stop on unrelated container impact.
