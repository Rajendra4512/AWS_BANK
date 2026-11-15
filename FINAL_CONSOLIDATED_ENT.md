# AWS_BANK — FINAL CONSOLIDATED ENTERPRISE BANKING, AI ENGINEERING, AUTO EVALS & CLOUD DEPLOYMENT MASTER PROMPT

## 0. MISSION AND EXECUTION CONTRACT

PROJECT:

AWS_BANK

PROJECT ROOT:

C:\Users\raj45\OneDrive\Desktop\AWS_BANK_project\AWS_BANK_enterprise_v1\AWS_BANK

EXECUTION MODE:

CONTINUE EXISTING IMPLEMENTATION — DO NOT RESTART FROM SCRATCH.

PRIMARY OBJECTIVE:

Transform AWS_BANK into a realistic, fully functional synthetic digital banking application with a separately secured enterprise AI administration platform.

The platform must support:

1. Professional Banking Portal
2. Secure Admin Console
3. User and role management
4. Persistent synthetic banking operations
5. Fraud and credit risk ML
6. AML investigation workflows
7. MLOps Control Center
8. Model Registry
9. Drift Monitoring
10. LLMOps Gateway
11. GenAI Configuration
12. RAG engineering where authorized and implemented
13. Agentic AI and Human-in-the-Loop governance
14. Automated AI Evaluations
15. AI Governance
16. Audit and Security
17. Advanced AI Engineering Learning Lab
18. AWS deployment readiness
19. Azure deployment readiness
20. Local Docker resource optimization

This must be a working application, not a collection of mock dashboards.

Banking operations must use persistent synthetic data.

AI features must have genuine backend integration.

All functionality must be evidence-based.

The application must remain lightweight on existing hardware.

Cloud deployment must be prepared and documented, but no cloud resources may be provisioned without explicit approval.

---

# SECTION 1 — HANDOFF AND PRESERVATION

## 1.1 Existing work

Read the existing project rules, Git status, architecture documentation and execution checkpoints.

Preserve all completed work from:

- ui_modernization_logs/
- enterprise_enhancement_logs/
- learning_lab_enhancement_logs/
- enterprise_banking_ai_logs/

Do not delete previous logs.

Do not overwrite completed reports.

Do not discard uncommitted source changes.

Do not repeat completed implementation without a verified reason.

Do not run simultaneously with another agent modifying the same repository.

## 1.2 Baseline assessment

Before changing code:

- Inspect current project structure.
- Identify existing backend modules.
- Identify frontend technology.
- Identify API routes.
- Identify authentication implementation.
- Identify role handling.
- Identify persistence implementation.
- Identify current ML models.
- Identify LLM integrations.
- Identify current model registry.
- Identify drift monitoring.
- Identify existing evaluation functions.
- Identify existing Learning Lab.
- Identify Docker configuration.
- Identify existing tests.
- Identify missing dependencies.

Classify each feature:

IMPLEMENTED / PARTIAL / MISSING / BLOCKED.

Do not infer implementation from UI labels.

## 1.3 Tool discovery

Discover existing approved tools:

- Unslop
- Graphify
- Archify
- Playwright
- Static analysis tools
- Existing testing utilities

Use Unslop for UI and learning-content quality.

Use Graphify for code dependencies, architecture and data flows.

Use Archify for architecture assessment and design decisions.

Do not claim tool usage without evidence.

Do not silently install missing tools.

Verify provenance and request approval for third-party installations.

## 1.4 Token efficiency

- Search filenames first.
- Search imports and symbols.
- Read only relevant code.
- Reuse previous reports.
- Avoid repeated full repository scans.
- Avoid reading unchanged files repeatedly.
- Reuse existing packages.
- Reuse existing components.
- Avoid unnecessary refactoring.
- Use targeted tests.
- Use checkpoints.
- Avoid unnecessary Docker builds.
- Keep progress updates concise.

Do not compromise quality or security to save tokens.

---

# SECTION 2 — ARCHITECTURE

## 2.1 Target architecture

Use a lightweight modular monolith.

Preserve:

- Python 3.11
- FastAPI
- Existing frontend framework
- Existing ML dependencies
- Existing Docker setup
- Existing database until approved migration
- Existing model artifacts
- Host port 7005
- Offline Python wheel installation

Do not introduce microservices automatically.

Do not introduce Kubernetes, Kafka, Spark, Redis, Celery, a standalone MLflow server or a separate vector database without approval.

## 2.2 Required domain boundaries

Organize functionality into logical modules:

- Identity
- Authorization
- Customer Management
- Banking Accounts
- Ledger
- Transfers
- Beneficiaries
- Statements
- Service Requests
- Fraud
- Credit Risk
- AML
- Model Training
- Model Inference
- Model Registry
- Drift Monitoring
- MLOps
- LLMOps
- GenAI
- RAG
- Agentic Workflows
- Auto Evals
- AI Governance
- Audit
- Learning Lab
- Cloud Deployment Configuration

Do not create empty modules solely to match this list.

Only introduce boundaries that support real functionality.

## 2.3 Two separate experiences

### Banking Portal

For customers and authorized bank staff.

Must resemble a modern professional digital bank.

### Admin & AI Control Center

For administrators, AI engineers, MLOps operators and governance personnel.

Must resemble an enterprise AI operations platform.

Both portals share one secure identity backend.

Use separate login routes and navigation.

Enforce permissions on backend endpoints.

Never rely only on hidden frontend menus.

---

# SECTION 3 — BANKING PORTAL

## 3.1 Data policy

Use synthetic customer identities and simulated money.

The application must behave like a real banking application.

Do not use real banking integrations.

Do not claim actual financial services.

### Initial data

Create a small idempotent seed dataset:

- Preserve existing admin account.
- 2–3 synthetic customers.
- 1–2 staff users where useful.
- A few savings/current accounts.
- 5–10 transactions per sample customer.
- A few beneficiaries.
- A few service requests.

Do not create massive test datasets.

Do not recreate records on each startup.

Do not reset existing data.

### Normal data

After initialization, user-created records must persist normally.

Do not delete normal banking data after tests.

Keep automated test fixtures isolated.

## 3.2 Customer functionality

Implement or complete:

- Customer dashboard
- Account summary
- Savings/current account views
- Available balance
- Transaction history
- Internal transfers
- Beneficiary management
- Simulated deposits
- Simulated withdrawals
- Statements
- Profile management
- Password change
- Service requests
- Notifications where supported

All buttons must perform genuine backend operations.

Do not display static fake balances.

## 3.3 Transfers and ledger

Use exact monetary arithmetic.

Prefer integer minor currency units or controlled decimal values.

Never use floating-point balances.

Require:

- Account ownership verification
- Destination validation
- Sufficient funds
- Amount limits
- Atomic debit/credit
- Idempotency
- Unique transaction identifiers
- Concurrency safety
- Transaction history
- Audit logging
- Balance reconciliation

A failed transfer must not partially post.

AI models must never directly authorize or execute transfers.

## 3.4 Staff operations

Authorized staff may:

- Look up permitted customers
- Review accounts
- Process service requests
- Investigate suspicious activity
- Review authorized risk information
- Manage assigned AML cases

Enforce least privilege and record sensitive actions.

## 3.5 Banking UI

Use:

- Professional corporate branding
- Clear account cards
- Readable balances
- Transaction tables
- Transfer forms
- Beneficiary screens
- Statement views
- Profile screens
- Responsive navigation
- Accessible controls

Display an unobtrusive:

"Simulated Banking Environment"

Do not expose internal AI configuration to ordinary customers.

---

# SECTION 4 — AUTHENTICATION, RBAC AND USER ADMINISTRATION

## 4.1 Identity

Use one secure identity backend.

Provide:

- Banking Portal login
- Admin Console login
- Logout
- Session expiration
- Password change
- Secure password reset
- Authorized user creation
- Account activation/deactivation

Preserve existing administrator access.

Do not create hardcoded backdoors.

## 4.2 Roles

Recommended roles:

- Customer
- Bank Officer
- Risk Analyst
- AI/MLOps Operator
- AI Governance Officer
- Bank Admin
- Super Admin

Define a centralized permission matrix.

Apply authorization to every sensitive API.

Apply object-level access checks.

## 4.3 Role switching

Allow switching only among roles already assigned to the user.

Validate every role switch server-side.

Record privileged role changes.

Do not permit self-promotion.

## 4.4 User management

Authorized administrators must be able to:

- Create users
- View users
- Activate/deactivate users
- Assign roles
- Revoke roles
- Initiate password resets
- Require password changes
- Revoke sessions where supported
- Review audit records

Never display existing passwords.

Never store plaintext passwords.

Use approved password hashing.

Use expiring, single-use reset tokens.

Protect privileged operations with recent authentication or step-up verification where feasible.

---

# SECTION 5 — AI/ML ENGINEERING

## 5.1 ML technologies

Audit and use existing:

- Python
- NumPy
- SciPy
- scikit-learn
- Pydantic
- FastAPI
- Existing serialization packages
- Existing model artifacts

Do not assume every model is trained.

Identify heuristic versus trained model implementations.

## 5.2 ML development

Support or document the complete workflow:

Data ingestion
→ Data validation
→ Feature engineering
→ Training
→ Evaluation
→ Artifact creation
→ Registry
→ Approval
→ Deployment
→ Inference
→ Monitoring
→ Drift detection
→ Retraining.

Where development functionality is implemented, use reproducible scripts.

Document model inputs, outputs, algorithms and limitations.

## 5.3 Fraud scoring

Implement or verify:

- Input validation
- Feature preparation
- Model execution
- Risk score
- Threshold-based outcome
- Model version
- Explanation where supported
- Inference audit
- Monitoring events

Never claim a heuristic score is a calibrated fraud probability.

## 5.4 Credit risk

Implement or verify:

- Input schema
- Feature transformations
- Risk scoring
- Model/heuristic identification
- Output explanation
- Version tracking
- Evaluation evidence

Do not claim probability of default without a validated calibrated model.

## 5.5 AML

Implement or verify:

- Suspicious activity indicators
- Alert creation
- Case management
- Case assignment
- Investigation status
- Review history
- Audit trail

AI-generated suggestions must not replace authorized investigation decisions.

---

# SECTION 6 — MLOPS CONTROL CENTER

## 6.1 Required features

- Model inventory
- Model versions
- Model artifact metadata
- Model evaluation results
- Model approval state
- Active model identification
- Model monitoring
- Drift monitoring
- Configuration management
- Rollback controls
- Audit history

## 6.2 Runtime parameters

Support backend-managed settings where implemented:

- Active approved model
- Inference threshold
- Monitoring thresholds
- Drift thresholds
- Alert thresholds
- Evaluation gates
- Monitoring frequency where supported
- Approved rollback targets

Every change must be:

- Authenticated
- Authorized
- Validated
- Versioned
- Persisted
- Audited
- Effective for subsequent requests where safe
- Reversible

Do not restart the container for ordinary supported configuration changes.

Do not hot-swap unapproved model artifacts.

## 6.3 Drift

Support meaningful drift calculations.

Distinguish:

- Data drift
- Prediction drift
- Concept drift
- Performance degradation

Do not claim concept drift without appropriate labels and outcome evidence.

Use real calculations, not fabricated chart values.

## 6.4 Model promotion

Require:

- Approved artifact
- Compatible input schema
- Evaluation evidence
- Quality-gate results
- Authorized approval
- Rollback target
- Audit record

Do not automatically promote models solely because a training run completes.

---

# SECTION 7 — LLMOPS GATEWAY

## 7.1 Provider abstraction

Support approved external LLM providers through existing integration mechanisms.

Do not require a local LLM.

Use BYOK where implemented.

## 7.2 Runtime parameters

Expose supported backend-managed settings:

- Provider
- Model identifier
- Temperature
- Maximum output tokens
- Timeout
- Retry policy
- Token budget
- Cost ceiling
- Prompt version
- Evaluation configuration
- Tracing configuration
- Safety settings

Validate provider-specific compatibility.

Do not assume identical settings across all models.

## 7.3 Secrets

- Mask API keys.
- Never return complete secrets.
- Never log credentials.
- Support authorized rotation.
- Restrict key management.
- Do not invoke paid APIs without approval.

If secure secret storage is not available, report the blocker.

## 7.4 Observability

Record where available:

- Request identifier
- Provider
- Model
- Prompt version
- Configuration version
- Latency
- Token usage
- Estimated cost
- Error category
- Evaluation status

Avoid recording sensitive prompt content unnecessarily.

---

# SECTION 8 — GENAI, RAG AND AGENTIC AI

## 8.1 GenAI

Provide controlled configuration for:

- Prompt templates
- Prompt versions
- Structured output schemas
- Approved model selection
- Guardrails
- Tool permissions
- Human approval

Do not permit AI-generated text to change balances, permissions or financial records without deterministic authorization.

## 8.2 RAG

Where authorized and implemented, support:

- Document ingestion
- Parsing
- Chunking
- Embeddings
- Retrieval
- Context assembly
- Grounded generation
- Citations
- Access controls
- Evaluation

Do not introduce a heavy vector database automatically.

For a small local dataset, evaluate lightweight retrieval approaches first.

Do not claim RAG is operational if only an architecture diagram exists.

## 8.3 Agentic AI

Support or document:

- Agent planning
- Tool calling
- Workflow state
- Tool authorization
- Human-in-the-Loop
- Retry policies
- Checkpointing
- Idempotency
- Failure recovery
- Agent evaluation

LangGraph and MCP are optional implementation technologies.

Do not claim integration without actual code and tests.

## 8.4 Human-in-the-Loop

Require human approval for sensitive actions.

Never allow autonomous agents to:

- Transfer funds
- Modify balances
- Grant roles
- Activate unapproved models
- Change security policies
- Delete records

Use deterministic backend authorization.

---

# SECTION 9 — AUTOMATED AI EVALUATIONS

## 9.1 Mandatory module

Create a restricted Admin Console module:

**AI Evaluation & Quality Engineering**

This is a core platform feature, not merely a Learning Lab topic.

## 9.2 Required tabs

- Evaluation Overview
- Evaluation Datasets
- ML Model Evals
- LLM Evals
- RAG Evals
- Agent Evals
- Safety & Security Evals
- Regression Comparison
- Evaluation Runs
- Quality Gates
- Evaluation Reports

Every enabled tab must have working backend functionality.

Mark unsupported capabilities clearly.

Do not fabricate evaluation scores.

## 9.3 Golden datasets

Use small, versioned synthetic evaluation datasets.

Start with approximately 30–50 representative cases for an initial comprehensive suite where applicable.

Include:

- Normal ML predictions
- Fraud edge cases
- Credit risk edge cases
- Known-answer LLM questions
- Insufficient-evidence questions
- Prompt injection cases
- Tool authorization cases
- Failure cases
- Boundary cases

Do not use real customer financial data.

## 9.4 Evaluation engine

Implement a lightweight local evaluation runner.

Support:

- Manual evaluation
- Bounded regression evaluation
- Candidate-versus-baseline comparison
- Evaluation history
- Case-level results
- Configurable thresholds
- Quality-gate decisions
- Report export
- Governance approval

Avoid heavy queue infrastructure.

Bound concurrency, execution time and memory.

## 9.5 ML evaluation metrics

Support applicable:

- Precision
- Recall
- F1
- PR-AUC
- ROC-AUC
- Confusion matrix
- False-positive rate
- False-negative rate
- Calibration
- Business-cost evaluation

Do not calculate metrics without suitable ground truth.

## 9.6 LLM evaluation metrics

Support applicable:

- Answer correctness
- Relevance
- Completeness
- Groundedness
- Unsupported claims
- Hallucination indicators
- Latency
- Token usage
- Estimated cost

Use deterministic checks where possible.

LLM-as-a-Judge must be optional, authorized and cost-controlled.

Do not treat judge scores as unquestionable truth.

## 9.7 RAG evaluation

Support where a real RAG pipeline exists:

- Recall@K
- MRR
- Retrieval relevance
- Groundedness
- Citation validity
- Abstention correctness

## 9.8 Agent evaluation

Support where agent workflows exist:

- Task success
- Tool-call correctness
- Unauthorized tool attempts
- HITL compliance
- Failure recovery
- Latency
- Cost

## 9.9 Security evaluation

Include:

- Prompt injection tests
- Sensitive-data leakage checks
- Unauthorized tool-call attempts
- Role-boundary tests
- Malformed input tests
- Unsafe output checks

Use safe synthetic test cases.

## 9.10 Quality gates

Make thresholds configurable and versioned.

Examples:

- Minimum model recall
- Maximum false-positive rate
- Maximum unsupported-answer rate
- Minimum groundedness
- Maximum latency
- Maximum evaluation cost
- Zero unauthorized tool executions

Use thresholds appropriate to the model and use case.

Do not invent universal production thresholds.

Failed mandatory gates must block automatic promotion.

## 9.11 Auto Evals integration

Integrate evaluation evidence with:

- Model Registry
- MLOps
- LLMOps
- GenAI
- Drift Monitoring
- AI Governance
- Audit Log

When a model or prompt changes, support controlled regression evaluation.

Do not execute unbounded evaluations.

Do not automatically invoke paid external APIs.

## 9.12 Evaluation audit

Record:

- Evaluation ID
- Dataset version
- Model/prompt version
- Configuration version
- Evaluation timestamp
- Metrics
- Case-level results
- Quality-gate decisions
- Approval status
- Evidence references

Do not fabricate evidence.

---

# SECTION 10 — AI GOVERNANCE

## 10.1 Governance center

Provide:

- Model inventory
- Model ownership
- Model purpose
- Risk classification
- Evaluation evidence
- Approval status
- Policy versions
- Configuration history
- Human review
- Audit trails
- Rollback history
- Operational exceptions

## 10.2 Approval controls

Require authorized approval for high-risk changes.

Prevent self-approval where separation of duties applies.

Record approval decisions.

Do not claim regulatory certification.

## 10.3 Security

Implement:

- Authentication
- RBAC
- Object-level authorization
- Input validation
- Session protection
- Secure password management
- Secret protection
- Audit logging
- Rate limiting where feasible
- CSRF protection where applicable
- Safe error handling
- Privileged-action verification

Never expose internal AI controls to customers.

---

# SECTION 11 — LEARNING LAB: AI ENGINEERING ACADEMY

## 11.1 Objective

Build a detailed beginner-to-architect learning experience.

The primary subjects are:

AI development, Python, ML, MLOps, LLMOps, GenAI, RAG, Agentic AI, Auto Evals, architecture, security and cloud deployment.

Banking is the practical application domain.

Do not focus primarily on banking processes.

The Learning Lab must be visible only to authorized administrator roles.

## 11.2 Curriculum

Include detailed tracks:

1. AI and ML fundamentals
2. Python for AI development
3. Python project architecture
4. Data engineering
5. Feature engineering
6. Model training
7. Model evaluation
8. ML inference
9. MLOps architecture
10. Model registry
11. Drift monitoring
12. LLM engineering
13. LLMOps
14. RAG engineering
15. Agentic AI
16. Multi-agent orchestration
17. MCP and tool integration
18. Automated AI evaluations
19. LLM-as-a-Judge
20. AI governance
21. AI security
22. FastAPI for AI
23. Docker and DevOps
24. AWS AI deployment
25. Azure AI deployment
26. AWS_BANK source-code architecture
27. Enterprise AI system design
28. End-to-end AI engineering capstone

Split large topics into substantive lessons.

Do not create empty curriculum placeholders.

## 11.3 Mandatory lesson structure

Every substantive lesson must explain:

1. What the concept is.
2. Why it is needed.
3. What problem it solves.
4. Where it fits into architecture.
5. Beginner terminology.
6. Technical theory.
7. Component responsibilities.
8. Architecture diagram.
9. Data flow.
10. Sequence flow.
11. Inputs.
12. Processing.
13. Outputs.
14. Python packages.
15. Actual Python scripts.
16. Classes and functions.
17. Configuration.
18. Execution commands.
19. Expected output.
20. Testing.
21. Debugging.
22. Failure scenarios.
23. Security.
24. Scalability.
25. Performance.
26. Cost.
27. Design alternatives.
28. Architecture trade-offs.
29. Practical exercises.
30. Knowledge checks.
31. Interview questions.
32. Official references.

Do not substitute generic summaries for detailed teaching.

## 11.4 Source-code walkthrough

Use actual AWS_BANK source files.

For each relevant Python module explain:

- File path
- Purpose
- Imports
- Classes
- Functions
- Parameters
- Return values
- Execution sequence
- Dependencies
- Error handling
- Testing
- Architecture placement

Never invent source files.

## 11.5 Architecture diagrams

Include:

- System context
- Logical architecture
- Component architecture
- API flow
- Authentication flow
- Banking transaction flow
- Model training flow
- Model inference flow
- MLOps lifecycle
- LLMOps lifecycle
- Auto Evals pipeline
- RAG architecture
- Agent orchestration
- Governance approval flow
- Docker topology
- AWS architecture
- Azure architecture

Clearly label:

CURRENT IMPLEMENTATION
EDUCATIONAL REFERENCE
PROPOSED ENHANCEMENT

Do not present planned infrastructure as deployed.

## 11.6 Practical exercises

Every exercise must include:

- Objective
- Prerequisites
- Required packages
- Source files
- Sample input
- Setup commands
- Execution commands
- Expected output
- Explanation
- Verification
- Troubleshooting
- Cleanup

Use synthetic data.

Avoid arbitrary code execution through the application.

## 11.7 Learning progress

Support persistent user-scoped progress:

- Track completion
- Lesson completion
- Resume learning
- Last visited lesson
- Exercise status
- Knowledge-check results where implemented

Do not equate clicking "Complete" with passing an exercise.

---

# SECTION 12 — CLOUD DEPLOYMENT READINESS

## 12.1 Critical requirement

AWS_BANK must be architecturally ready for deployment to either AWS or Azure.

Do not deploy automatically.

Do not provision cloud resources without approval.

Do not incur cloud charges without approval.

## 12.2 Cloud-readiness assessment

Audit:

- Docker image
- Environment configuration
- Secrets
- Database persistence
- Model artifact storage
- File uploads
- Logs
- Health endpoints
- Readiness checks
- Stateless application behavior
- Session handling
- Reverse proxy compatibility
- HTTPS
- Authentication
- Resource limits
- Startup/shutdown behavior
- Graceful termination
- Backup and restore
- Database migrations
- CI/CD
- Rollback
- Observability

Record cloud blockers.

## 12.3 Twelve-factor configuration

Move environment-specific settings into validated configuration.

Do not hardcode:

- Secrets
- Database credentials
- Cloud resource names
- Internal hostnames
- Production URLs
- Provider API keys

Use secure secret injection.

Do not expose secrets in frontend bundles.

## 12.4 Database portability

The local environment may continue using SQLite.

For a multi-user cloud deployment, design and validate a supported migration path to managed PostgreSQL.

Do not assume SQLite on ephemeral container storage is suitable for production.

Prepare migration and rollback plans.

Do not execute migrations without approval.

## 12.5 Artifact portability

Support a documented path from local model artifacts to cloud object storage.

AWS target:

S3.

Azure target:

Blob Storage.

Do not hardcode local artifact paths into business logic.

Use a configurable storage abstraction where justified.

Preserve artifact integrity and version metadata.

## 12.6 Container portability

Prepare the existing image for managed container deployment.

Verify:

- Non-root execution
- Correct port binding
- Health checks
- Environment configuration
- Graceful shutdown
- Minimal dependencies
- No embedded secrets
- Persistent data separation
- Model loading
- CPU/memory behavior

Preserve the local offline-wheel build.

Document any changes needed for standard cloud builds.

## 12.7 CI/CD readiness

Prepare a minimal deployment pipeline design.

Include:

- Dependency checks
- Static analysis
- Unit tests
- API tests
- Security scanning
- Docker image build
- Image vulnerability scanning
- Artifact versioning
- Evaluation quality gates
- Deployment approval
- Rollback

Do not enable automatic production deployment without approval.

---

# SECTION 13 — AWS DEPLOYMENT ARCHITECTURE

## 13.1 Target options

Document two AWS deployment paths.

### Path A — Lightweight AWS_BANK deployment

Recommended starting architecture:

- ECR
- ECS/Fargate
- Application Load Balancer where required
- RDS PostgreSQL
- S3
- Secrets Manager
- CloudWatch
- IAM
- TLS/HTTPS

Select networking and ingress architecture based on actual requirements and cost.

### Path B — Advanced MLOps architecture

Reference architecture may include:

- SageMaker training
- SageMaker Model Registry
- SageMaker endpoints
- SageMaker monitoring
- S3 datasets
- EventBridge
- Step Functions
- CloudWatch
- IAM
- KMS
- CI/CD

Do not provision the advanced stack by default.

## 13.2 AWS deployment preparation

Prepare:

- Architecture diagram
- Resource inventory
- Dependency map
- Configuration template
- Secrets inventory
- IAM permission design
- Network design
- Database migration plan
- Artifact storage plan
- Container deployment plan
- Monitoring plan
- Backup plan
- Rollback plan
- Cost estimation methodology
- Cleanup plan

## 13.3 AWS deployment stages

Document step-by-step:

1. Create/configure AWS account.
2. Enable MFA.
3. Configure billing alerts and budgets.
4. Configure IAM.
5. Select region.
6. Configure networking.
7. Prepare container image.
8. Create ECR repository.
9. Authenticate Docker to ECR.
10. Push image.
11. Prepare RDS PostgreSQL.
12. Prepare S3 storage.
13. Configure Secrets Manager.
14. Configure ECS/Fargate service.
15. Configure networking and ingress.
16. Configure HTTPS.
17. Run approved migrations.
18. Deploy application.
19. Verify health endpoints.
20. Verify authentication.
21. Verify banking workflows.
22. Verify AI inference.
23. Verify Auto Evals.
24. Verify logs and monitoring.
25. Test backup and rollback.
26. Review security and costs.
27. Document cleanup.

Provide accurate command templates with placeholders.

Do not invent account IDs or resource names.

---

# SECTION 14 — AZURE DEPLOYMENT ARCHITECTURE

## 14.1 Target options

Document two Azure deployment paths.

### Path A — Lightweight AWS_BANK deployment

Recommended starting architecture:

- Azure Container Registry
- Azure Container Apps
- Azure Database for PostgreSQL
- Azure Blob Storage
- Azure Key Vault
- Managed Identity
- Azure Monitor
- Application Insights
- Entra ID/RBAC

Select networking and ingress architecture based on requirements and cost.

### Path B — Advanced Azure MLOps

Reference architecture may include:

- Azure Machine Learning
- MLflow tracking
- Azure ML Model Registry
- Managed endpoints
- Blob Storage
- Azure Monitor
- Key Vault
- CI/CD
- Infrastructure as Code

Do not provision advanced services automatically.

## 14.2 Azure deployment preparation

Prepare:

- Architecture diagram
- Resource inventory
- Resource group design
- Identity and RBAC design
- Networking
- Container configuration
- Database migration plan
- Artifact storage plan
- Secrets configuration
- Monitoring
- Backup
- Rollback
- Cost estimation methodology
- Cleanup

## 14.3 Azure deployment stages

Document step-by-step:

1. Configure Azure subscription.
2. Verify credits and billing.
3. Configure budget alerts.
4. Create resource group.
5. Configure identity and RBAC.
6. Select region.
7. Configure networking.
8. Prepare container image.
9. Create Azure Container Registry.
10. Push image.
11. Configure PostgreSQL.
12. Configure Blob Storage.
13. Configure Key Vault.
14. Configure managed identity.
15. Configure Container Apps.
16. Configure ingress and HTTPS.
17. Run approved migrations.
18. Deploy application.
19. Verify health endpoints.
20. Verify authentication.
21. Verify banking workflows.
22. Verify AI inference.
23. Verify Auto Evals.
24. Configure monitoring.
25. Verify backup and rollback.
26. Review security and costs.
27. Document cleanup.

Provide accurate Azure CLI or infrastructure templates.

Do not invent subscription IDs.

---

# SECTION 15 — LEARNING LAB CLOUD DEPLOYMENT COURSE

## 15.1 Mandatory requirement

The Learning Lab must include detailed, beginner-friendly AWS and Azure deployment courses based on the actual AWS_BANK application.

These courses must not consist only of architecture diagrams or service descriptions.

They must teach the learner how to deploy the application step by step.

## 15.2 AWS lesson requirements

For every AWS deployment stage explain:

- What the AWS service is.
- Why it is required.
- Where it fits in the architecture.
- What it costs conceptually.
- Prerequisites.
- Required permissions.
- Input configuration.
- Setup instructions.
- Commands.
- Expected results.
- Verification.
- Troubleshooting.
- Security.
- Rollback.
- Cleanup.

Include detailed AWS_BANK-specific examples.

Explain how SageMaker differs from ECS-hosted inference.

Explain when SageMaker is justified.

## 15.3 Azure lesson requirements

For every Azure deployment stage explain:

- What the Azure service is.
- Why it is required.
- Where it fits in the architecture.
- Prerequisites.
- Identity and RBAC.
- Input configuration.
- Setup instructions.
- Commands.
- Expected results.
- Verification.
- Troubleshooting.
- Security.
- Rollback.
- Cleanup.

Include AWS_BANK-specific examples.

Explain Azure ML versus Container Apps inference.

## 15.4 Cloud architecture comparison

Compare:

- AWS IAM vs Azure RBAC
- ECR vs ACR
- ECS/Fargate vs Container Apps
- S3 vs Blob Storage
- RDS vs Azure Database for PostgreSQL
- SageMaker vs Azure ML
- Secrets Manager vs Key Vault
- CloudWatch vs Azure Monitor
- AWS CI/CD options vs Azure/GitHub workflows

Explain cost, complexity, scalability, security and operational trade-offs.

## 15.5 Cloud deployment evidence

Distinguish:

- DOCUMENTED
- LOCALLY VALIDATED
- CLOUD VALIDATED
- BLOCKED
- NOT TESTED

Never claim cloud deployment was verified if no cloud resources were actually deployed.

---

# SECTION 16 — UI/UX

## 16.1 Banking Portal

Use a professional banking design.

Include:

- Account dashboard
- Transaction history
- Transfers
- Beneficiaries
- Statements
- Profile
- Service requests
- Notifications

Use consistent typography and accessible forms.

## 16.2 Admin Console

Use a distinct enterprise operations design.

Include:

- Operations Overview
- User Management
- Banking Administration
- Fraud & Risk
- Model Registry
- MLOps
- Drift Monitoring
- LLMOps
- GenAI
- Auto Evals
- AI Governance
- Audit
- Learning Lab
- Cloud Readiness

Use meaningful status indicators and actual data.

## 16.3 UI quality

Use Unslop where available.

Avoid generic AI-generated visual styling.

Use appropriate icons.

Support responsive layouts.

Verify loading, empty, success and error states.

Do not create decorative nonfunctional buttons.

---

# SECTION 17 — LOCAL HARDWARE OPTIMIZATION

## 17.1 Target hardware

- Windows
- Intel Core i5-1235U
- 24 GB RAM
- Docker Desktop
- No dedicated GPU
- Other running application containers

## 17.2 Runtime design

Prefer:

- One FastAPI container
- Existing Python packages
- Existing database
- Local scikit-learn inference
- Lazy model loading
- Bounded caches
- Single worker initially
- Small synthetic datasets
- Paginated queries
- Bounded evaluation jobs
- Optional external LLM APIs

Do not require local large-model inference.

Do not introduce heavy services automatically.

Measure CPU and memory usage.

## 17.3 Docker protection

Protect all unrelated Docker applications.

Never run global cleanup.

Never stop unrelated containers.

Never delete unrelated volumes or networks.

Preserve port 7005.

Preserve offline wheel installation.

Do not rebuild/restart AWS_BANK without approval.

Use targeted source-level testing first.

---

# SECTION 18 — TESTING AND QUALITY GATES

## 18.1 Required testing

Perform:

- Unit tests
- API tests
- Authentication tests
- RBAC tests
- Banking workflow tests
- Financial integrity tests
- ML inference tests
- MLOps configuration tests
- LLMOps configuration tests
- Auto Evals tests
- Governance tests
- Learning Lab tests
- Browser tests
- Resource usage tests
- Cloud readiness checks

## 18.2 Financial integrity

Verify:

- Correct balances
- Atomic transfers
- Idempotency
- Insufficient funds
- Unauthorized access
- Concurrent transfers
- Reconciliation
- Persistence

## 18.3 AI quality

Verify:

- Model execution
- Correct model version
- Correct configuration version
- Input validation
- Output validation
- Evaluation metrics
- Quality gates
- Baseline comparison
- Drift calculations
- Audit records

## 18.4 Negative testing

Test:

- Unauthorized API access
- Role escalation attempts
- Invalid banking operations
- Invalid model settings
- Missing model artifacts
- LLM provider failures
- Evaluation timeout
- Invalid evaluation datasets
- Failed quality gates
- Secret exposure attempts

## 18.5 Test reporting

Use:

PASS / PARTIAL / FAIL / BLOCKED / NOT TESTED.

Every PASS must have actual execution evidence.

Do not fabricate results.

---

# SECTION 19 — LOGS AND CHECKPOINTS

## 19.1 Primary log directory

Use:

`enterprise_banking_ai_logs/`

Preserve all historical logs.

## 19.2 Required structure

enterprise_banking_ai_logs/
- 00_HANDOFF_BASELINE.md
- 01_TOOL_DISCOVERY.md
- 02_ARCHITECTURE_ASSESSMENT.md
- 03_TARGET_ARCHITECTURE.md
- 04_ROLE_PERMISSION_MATRIX.md
- 05_BANKING_FEATURES.md
- 06_SYNTHETIC_DATA_STRATEGY.md
- 07_LEDGER_DESIGN.md
- 08_USER_MANAGEMENT.md
- 09_MLOPS_CONFIGURATION.md
- 10_LLMOPS_CONFIGURATION.md
- 11_GENAI_GOVERNANCE.md
- 12_LEARNING_LAB.md
- 13_API_INTEGRATION.md
- 14_SECURITY_RBAC.md
- 15_FUNCTIONAL_TESTS.md
- 16_FINANCIAL_INTEGRITY_TESTS.md
- 17_AI_VALIDATION.md
- 18_RESOURCE_USAGE.md
- 19_DEFECT_TRACKER.md
- 20_MIGRATION_PROPOSALS.md
- 21_DEPLOYMENT_READINESS.md
- 22_FINAL_ACCEPTANCE.md
- 23_AUTO_EVALS_ARCHITECTURE.md
- 24_EVALUATION_DATASETS.md
- 25_EVALUATION_METRICS.md
- 26_EVALUATION_EXECUTION.md
- 27_EVALUATION_QUALITY_GATES.md
- 28_AUTO_EVALS_TEST_RESULTS.md
- 29_CLOUD_READINESS_ASSESSMENT.md
- 30_AWS_DEPLOYMENT_ARCHITECTURE.md
- 31_AZURE_DEPLOYMENT_ARCHITECTURE.md
- 32_AWS_DEPLOYMENT_RUNBOOK.md
- 33_AZURE_DEPLOYMENT_RUNBOOK.md
- 34_CLOUD_SECURITY_AND_COST.md
- 35_CI_CD_READINESS.md
- 36_LEARNING_LAB_CLOUD_COURSE.md
- 37_FINAL_CONSOLIDATED_ACCEPTANCE.md
- EXECUTION_CHECKPOINT.md
- feature_logs/
- defects/
- evidence/
- cloud/
- auto_evals/

## 19.3 Checkpoint format

Record:

- Timestamp
- Phase
- Completed tasks
- Pending tasks
- Modified files
- Tests executed
- Test results
- Defects
- Blockers
- Approval requirements
- Next safe action

Resume from the latest verified checkpoint.

Do not repeat completed work unnecessarily.

## 19.4 Defects

Record each verified defect separately with:

- ID
- Severity
- Feature
- Reproduction
- Expected result
- Actual result
- Root cause
- Fix
- Verification
- Status

Do not hide defects to declare success.

---

# SECTION 20 — EXECUTION PLAN

## Phase 1 — Handoff

Read checkpoints and establish the baseline.

## Phase 2 — Architecture

Define the two-portal architecture, permissions, AI components and cloud portability.

## Phase 3 — Identity

Complete secure authentication, roles and user management.

## Phase 4 — Banking

Implement persistent synthetic banking workflows.

## Phase 5 — Ledger

Verify financial integrity and transaction safety.

## Phase 6 — Admin Console

Complete operational administration.

## Phase 7 — ML/MLOps

Complete model inference, registry, monitoring and runtime configuration.

## Phase 8 — LLMOps/GenAI

Complete supported provider configuration, prompts, guardrails and observability.

## Phase 9 — Auto Evals

Implement golden datasets, evaluation runners, metrics, quality gates and regression comparison.

## Phase 10 — Governance/HITL

Implement approvals, policies, evaluation evidence and audit.

## Phase 11 — AI Integration

Connect authorized AI capabilities to banking workflows.

## Phase 12 — Learning Lab

Complete detailed AI Engineering, Python, MLOps, LLMOps, Auto Evals, RAG, Agentic AI and architecture lessons.

## Phase 13 — Cloud Readiness

Prepare configuration, storage, database portability, container deployment and CI/CD.

## Phase 14 — AWS Deployment Course

Create detailed AWS_BANK-specific AWS deployment lessons and runbooks.

## Phase 15 — Azure Deployment Course

Create detailed AWS_BANK-specific Azure deployment lessons and runbooks.

## Phase 16 — Testing

Run security, banking, AI, evaluation, integration and resource tests.

## Phase 17 — Final Acceptance

Produce evidence-backed completion and readiness reports.

Do not stop after writing plans.

Continue safe implementation until the authorized scope is complete or blocked.

---

# SECTION 21 — APPROVAL GATES

Explicit approval is required before:

- Database schema migration
- Destructive data operations
- Unapproved dependency installation
- Framework replacement
- Authentication architecture replacement
- AWS/Azure resource provisioning
- Paid API invocation
- Cloud spending
- Docker container restart/recreation
- Production deployment
- Changes outside the AWS_BANK repository

If blocked:

1. Document the exact blocker.
2. Explain why approval is required.
3. Describe impact.
4. Provide rollback.
5. Continue independent safe work.
6. Request approval for the restricted action.

Do not bypass approval gates.

---

# SECTION 22 — FINAL ACCEPTANCE

## Banking

Verify that customers can:

- Sign in
- View accounts
- View balances
- Add beneficiaries
- Transfer simulated money
- View transaction history
- Download statements
- Create service requests
- Change passwords
- Sign out
- Sign back in with persistent data

## Admin

Verify that authorized administrators can:

- Manage users
- Manage roles
- Initiate secure password resets
- Review banking operations
- Configure supported MLOps parameters
- Configure supported LLMOps parameters
- Manage GenAI configuration
- Run Auto Evals
- Review governance
- Review audit logs
- Access Learning Lab

## AI

Verify:

- Actual inference
- Correct model/configuration version
- Real evaluation metrics
- Regression comparison
- Quality-gate enforcement
- Monitoring
- Drift calculations
- Auditability
- Safe failure handling

## Learning Lab

Verify:

- Detailed technical lessons
- Actual source-code references
- Python examples
- Architecture diagrams
- Data flows
- MLOps lifecycle
- LLMOps lifecycle
- Auto Evals
- RAG
- Agentic AI
- AI governance
- AWS deployment course
- Azure deployment course
- Practical exercises
- Persistent learning progress

## Cloud

Verify:

- Container readiness
- Environment configuration
- Secrets design
- Database portability
- Artifact portability
- Health checks
- Monitoring
- CI/CD preparation
- AWS runbook
- Azure runbook
- Rollback procedures
- Cost controls

Do not claim CLOUD VALIDATED unless a real authorized deployment was tested.

## Final report

Provide:

- Completed features
- Partial features
- Blocked features
- Modified files
- Tools actually used
- Packages reused
- Tests executed
- Evidence
- Security findings
- Resource usage
- Cloud readiness
- Outstanding defects
- Required approvals
- Next recommended steps

Do not fabricate success.

---

# FINAL EXECUTION DIRECTIVE

Continue AWS_BANK from the latest verified checkpoint.

Preserve all previous work.

Use existing packages and infrastructure.

Use Unslop, Graphify and Archify when available.

Build a professional, genuinely functional synthetic Banking Portal.

Build a separately secured enterprise AI Admin Console.

Implement user management, password management and RBAC.

Complete ML inference, MLOps, Model Registry and Drift Monitoring.

Implement backend-driven runtime configuration for supported MLOps and LLMOps parameters.

Complete GenAI governance and controlled agentic workflows where authorized.

Implement Automated AI Evaluations as a first-class operational module.

Integrate evaluation evidence with model promotion and AI governance.

Build a deeply technical AI Engineering Learning Lab.

Explain actual Python scripts, model development, architecture, data flows, evaluation and deployment.

Prepare the application for AWS and Azure deployment.

Create detailed AWS and Azure deployment runbooks and Learning Lab courses.

Keep the application lightweight on existing hardware.

Protect unrelated Docker applications.

Maintain logs and checkpoints.

Run genuine tests.

Never claim success without evidence.

Do not perform restricted operations without approval.

**FINAL SUCCESS CRITERION: A functional synthetic banking platform, a separately secured enterprise AI/MLOps/LLMOps/Auto Evals administration system, an advanced AI Engineering Learning Lab, and a verified cloud-deployment-ready architecture with detailed AWS and Azure deployment instructions.**