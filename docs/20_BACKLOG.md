# Implementation backlog (prioritized, immutable scope baseline v1)

| ID | Story | Acceptance criteria | State |
|---|---|---|---|
| CORE-01 | Admin can provision users | Password hashed; admin-only; audit | Implemented baseline |
| MLOPS-01 | Train and compare fraud candidates | Precision, recall, F1, PR-AUC and artifacts | Implemented baseline |
| MLOPS-02 | Promote and roll back | One active version and audit | Implemented baseline |
| MLOPS-03 | Monitor drift | PSI history and threshold | Implemented baseline |
| MLOPS-04 | Native MLflow registry | Experiment run IDs, model versions, aliases and artifact lineage | Pending |
| MLOPS-05 | Evidently reports | Dataset snapshots, test suite and report storage | Pending |
| CREDIT-01 | Assess transparent credit risk | Input validation, index and reason codes | Implemented baseline |
| CREDIT-02 | Train calibrated PD model | Dataset lineage, validation, calibration, explainability | Pending |
| AML-01 | Create investigation cases | Deterministic rules and persistent case | Implemented baseline |
| AML-02 | Review cases | Different reviewer, audit and reason | Implemented baseline |
| AML-03 | Anomaly model and alert feedback | Train/evaluate and analyst feedback | Pending |
| LLM-01 | Offline knowledge gateway | Grounded curated answers, explicit provenance | Implemented baseline |
| LLM-02 | Bedrock adapter | IAM, inference, rate limits, cost, policy checks | Pending |
| EVAL-01 | Deterministic regression suite | Persist outcomes and failure cases | Implemented baseline |
| EVAL-02 | Grounding/safety judge | Curated labeled test set, rubric, human calibration | Pending |
| AGENT-01 | Maker-checker case review | Durable status, separation of duties | Implemented baseline |
| AGENT-02 | LangGraph orchestration | Checkpoints, interrupts, resume and safe tools | Pending |
| AWS-01 | Deploy to AWS | IaC, ECR, ECS, ALB, RDS, S3, Secrets Manager | Pending |
| SEC-01 | Production security controls | SSO/MFA, CSRF, rate limiting, immutable audit | Pending |
| LEARN-01 | Admin-editable learning lab | Code trace and real enterprise decisions | Implemented baseline; expand content |
