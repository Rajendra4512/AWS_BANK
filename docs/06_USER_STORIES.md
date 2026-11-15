# User stories and implementation backlog

Priority P0 (working MVP):

| ID | Story | Acceptance criteria | State |
|---|---|---|---|
| US-01 | As an admin I can bootstrap a secure account | Requires 12+ char secret; no embedded default | Implemented |
| US-02 | As a user I can authenticate | Cookie session, unauthorized 401 | Implemented |
| US-03 | As an admin I can create accounts | Admin-only route, duplicate 409, audit | Implemented |
| US-04 | As an admin I can train candidate | Reproducible model, metrics and version | Implemented |
| US-05 | As an admin I can promote or roll back | Exactly one active model, audit | Implemented |
| US-06 | As a user I can score a transaction | Validated inputs, probability + version | Implemented |
| US-07 | As an admin I can simulate drift | PSI result and alert threshold stored | Implemented |
| US-08 | As a user I can learn concepts | Lessons describe code and caveats | Implemented (starter lessons) |
| US-09 | As an admin I can maintain lessons | Content changes persist, audit | Implemented |
| US-10 | As an admin I can view operations | Audit and users visible in admin panel | Implemented |

Priority P1 (not implemented):

| ID | Story | Acceptance criteria |
|---|---|---|
| US-11 | As an ML engineer I can import Kaggle data | License review, schema mapping, leakage tests, PII policy, upload size cap |
| US-12 | As an operator I can see Evidently reports | Validated adapter, persisted report, history and resource test |
| US-13 | As an ML engineer I can use MLflow registry | Tracking server, run lineage, artifacts, model aliases, promotion integration |
| US-14 | As a risk approver I can enforce maker-checker | Distinct creator/approver identities, signed decision and rejection |
| US-15 | As a user I can view model explanations | Calibrated probabilities, SHAP/coefficients with warnings |
| US-16 | As an SRE I can deploy to AWS | Terraform/IaC, HTTPS, RDS/S3, IAM, backups, smoke tests |
| US-17 | As a learner I can follow code-linked exercises | File anchors, diagrams, exercises, expected outputs, quiz and progress |
| US-18 | As an admin I can disable accounts | Last-admin guard, session revocation, audit |

Priority P2 (not implemented):

| ID | Story | Acceptance criteria |
|---|---|---|
| US-19 | As an analyst I can use Bedrock explanations | Approved IAM, redaction, budget, guardrails, citations |
| US-20 | As an operator I can run automated LLM evaluations | Curated dataset, versioned rubrics, repeatable scores, judge calibration |
| US-21 | As a reviewer I can approve agent actions | Durable checkpoint, expiry, replay-safe resume, audit |
| US-22 | As an admin I can manage LLM provider gateway | Provider config, BYOK/role permissions, budgets, observability |
