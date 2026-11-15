# AWS_BANK AI Engineering Learning Lab

Status: local educational course map; synthetic data only. The current application is the executable reference. Proposed cloud and external-model components are labeled as reference architecture and are not deployed.

## How to use the course

Each lesson has a source anchor, a runnable or inspectable exercise, expected evidence, and a security boundary. Learners resume through `GET /api/learning/progress` and update state with `PUT /api/learning/progress/{slug}`. Completing a lesson does not imply that an exercise passed.

## Course map

| Track | Lesson | Source anchor | Practical evidence |
|---|---|---|---|
| Foundations | AI/ML terminology and lifecycle | `app/main.py:synthetic`, `docs/03_ARCHITECTURE.md` | Explain ingest → train → evaluate → promote → monitor |
| Foundations | Python modules and configuration | `app/main.py`, `app/domains.py` | Trace imports, environment variables and startup |
| Foundations | FastAPI routing and validation | `app/main.py`, `app/domains.py` | Send valid and invalid JSON; compare 200/401/422 |
| Data | Synthetic data generation | `app/main.py:synthetic` | Generate 100 rows and inspect shape/labels |
| Data | Feature engineering | `app/main.py:FEATURES` | Map transaction fields to the scoring vector |
| ML | Logistic regression baseline | `app/main.py:train` | Train a candidate and inspect metrics |
| ML | Precision, recall and PR-AUC | `app/main.py:train`, `app/domains.py:active_model_eval` | Explain imbalanced-class trade-offs |
| ML | Inference validation | `app/main.py:score` | Score a synthetic transaction and identify model version |
| MLOps | Registry states | `models` table, `app/main.py:promote` | Candidate → evaluation → active/rollback |
| MLOps | Quality gates | `app/domains.py:active_model_eval` | Observe a failed recall gate block promotion |
| MLOps | Drift monitoring | `app/main.py:psi`, `drift_check` | Run a bounded shift and inspect next action |
| MLOps | Artifact integrity boundary | `Dockerfile`, `artifacts/` | Explain why untrusted uploads cannot become models |
| LLMOps | Provider abstraction | `app/domains.py:Provider`, provider routes | Configure offline metadata without storing secrets |
| LLMOps | Budgets and observability | `app/domains.py:query`, `domain_events` | Trace a query event and its provider boundary |
| GenAI | Curated offline gateway | `app/domains.py:offline_answer` | Ask a known and unknown question |
| RAG | Retrieval and citations | `app/domains.py:retrieve_lessons`, `/api/rag/query` | Verify citation ranking and abstention |
| RAG | Recall@K and MRR | `app/domains.py:rag_eval` | Read the synthetic golden-set metrics |
| Agents | Maker-checker workflow | `app/domains.py:aml`, `review` | Show requester/reviewer separation |
| Agents | Tool authorization | `app/banking.py`, transfer route | Explain why AI routes cannot execute transfers |
| Auto Evals | Golden datasets | `app/domains.py:EVAL_SET` | Add a synthetic known-answer case |
| Auto Evals | ML evaluation | `app/domains.py:active_model_eval` | Inspect confusion matrix and calibration loss |
| Auto Evals | Safety evaluation | `app/domains.py:security_eval` | Run prompt-injection and tool-boundary cases |
| Governance | Audit and evidence | `audit` table, governance summary route | Correlate action, actor, timestamp and result |
| Governance | RBAC and reset tokens | `app/main.py` user routes | Reassign a role and issue a single-use reset token |
| Banking | Integer ledger design | `app/banking.py` | Reconcile debit/credit and idempotent replay |
| Banking | Ownership and staff access | `app/banking.py:_owns_account`, staff routes | Verify customer 403 and staff permitted lookup |
| Operations | Docker protections | `Dockerfile`, `compose.yaml` | Inspect non-root, read-only, limits, healthcheck |
| Cloud | AWS deployment boundary | `docs/21_AWS_DEPLOYMENT_RUNBOOK.md` | Review ECS/RDS/S3/Secrets Manager gates |
| Cloud | Azure deployment boundary | `docs/22_AZURE_DEPLOYMENT_RUNBOOK.md` | Review Container Apps/PostgreSQL/Key Vault gates |
| Capstone | End-to-end release review | `enterprise_banking_ai_logs/` | Produce a PASS/PARTIAL/BLOCKED evidence report |

## Mandatory lesson exercise structure

For each lesson, the instructor or learner records: objective, prerequisites, terminology, architecture placement, inputs, processing, outputs, source files, classes/functions, configuration, commands, expected output, tests, debugging, failure scenarios, security, scalability, performance, cost, alternatives, trade-offs, exercise result, knowledge check, interview question, and official reference links. A lesson is marked `passed` only after its evidence is reviewed.

## Core flows to draw and explain

1. Browser → session login → role-protected API → SQLite/audit.
2. Customer transfer → ownership check → `BEGIN IMMEDIATE` → debit/credit ledger → idempotency replay.
3. Train → candidate artifact → evaluation → quality gate → human promotion → score → drift.
4. RAG question → token retrieval → citations or abstention → audit event.
5. AML signal → pending case → independent reviewer → approved/rejected state.
6. Local image → CI tests/build scan → approved AWS/Azure migration → canary → rollback.

## Capstone acceptance

Use only synthetic identities and simulated money. Demonstrate a customer transfer, failed unauthorized transfer, statement, password rotation, role reassignment, model evaluation with a failed gate, RAG abstention, maker-checker review, and a healthy container. Attach evidence under `enterprise_banking_ai_logs/evidence/`. Do not provision cloud resources as part of the exercise.
