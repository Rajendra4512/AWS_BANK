# Delivery roadmap and decision gates

**Phase 0 — runnable local foundation (included):** FastAPI UI, auth, synthetic fraud classifier, local registry, PSI, admin editor, audit, constrained Docker.

**Phase 1 — production-quality local MLOps:** full end-to-end tests, UI workflows, user disable, CSRF/lockout, richer model evaluation, time-based validation, data import safeguards, model cards, version comparison, true Evidently integration, MLflow tracking/registry on optional external service. Gate: memory benchmark and no critical security defects.

**Phase 2 — governance and learning:** maker-checker, alert workflow, approval queue, training pipeline status, rollback drill, deep code-linked lessons, practical labs and quizzes. Gate: independent reviewer can reproduce decision trail.

**Phase 3 — AWS deployment:** PostgreSQL migration, S3 artifacts, IaC, ECS, ECR, ALB TLS, WAF, IAM, CloudWatch, backups, budgets, penetration test. Gate: cost approval and production-readiness review.

**Phase 4 — LLMOps/Bedrock:** provider-neutral gateway, Bedrock model selection, BYOK for non-AWS providers, token/cost monitoring, evaluation datasets, groundedness and LLM-as-judge calibration. Gate: PII policy and approved external inference.

**Phase 5 — Agentic HITL:** LangGraph optional service, checkpoint store, approval/deny/resume, idempotent external actions, evaluation, failure injection. Gate: explicit human authorization for every sensitive action.

**Challenge:** Do not bundle all four AI disciplines into the 1 GB MVP. A genuinely reliable end-to-end classic MLOps workflow is more compelling than four shallow dashboards.
