# AWS_BANK — FULL-STACK ENTERPRISE ENHANCEMENT & END-TO-END VALIDATION

## EXECUTION TYPE

CONTINUATION OF EXISTING AWS_BANK UI MODERNIZATION.

This is not a new project, rewrite or replacement of the previous execution.

The earlier frontend modernization task may already have modified files and created logs.

**MANDATORY: Preserve all previous work, logs, checkpoints, test evidence, existing functionality and application data.**

Do not start a second agent against the same working tree while the previous agent is still modifying it.

## 1. PRIMARY OBJECTIVE

Transform AWS_BANK into a fully integrated, functional, modern enterprise AI/MLOps learning and showcase platform.

The application must demonstrate real, executable workflows across:

1. Executive Overview
2. Fraud Scoring
3. Model Registry
4. Drift Monitoring
5. Credit Risk
6. AML & Cases
7. LLMOps
8. Learning Lab
9. Admin Console

Scope includes:

- Frontend
- Backend
- APIs
- Data persistence
- ML inference
- Model governance
- MLOps workflows
- LLMOps integrations
- Authentication and RBAC
- Audit logging
- Observability
- Testing
- Documentation
- Controlled deployment

All functionality must be implemented honestly.

Do not simulate successful operations when no real execution occurred.

Educational simulations are permitted only when clearly labeled and isolated from operational results.

## 2. PROJECT AND LOG LOCATIONS

Project root:

`C:\Users\raj45\OneDrive\Desktop\AWS_BANK_project\AWS_BANK_enterprise_v1\AWS_BANK`

Existing UI modernization logs:

`ui_modernization_logs/`

New full-stack logs:

`enterprise_enhancement_logs/`

Do not delete, overwrite or recreate existing logs.

Create the new directory only if it does not already exist.

Maintain references to existing modernization reports rather than duplicating them.

Required files:

- `00_HANDOFF_AND_BASELINE.md`
- `01_TOOL_AND_ARCHITECTURE_AUDIT.md`
- `02_FULL_STACK_GAP_ANALYSIS.md`
- `03_API_AND_DATA_FLOW_AUDIT.md`
- `04_FEATURE_IMPLEMENTATION_TRACKER.md`
- `05_MLOPS_VALIDATION.md`
- `06_LLMOPS_VALIDATION.md`
- `07_SECURITY_AND_RBAC.md`
- `08_FUNCTIONAL_TEST_RESULTS.md`
- `09_INTEGRATION_TEST_RESULTS.md`
- `10_DEFECT_TRACKER.md`
- `11_DOCKER_DEPLOYMENT.md`
- `12_FINAL_ACCEPTANCE.md`
- `EXECUTION_CHECKPOINT.md`
- `feature_logs/`
- `defects/`
- `evidence/`

Never overwrite historical evidence.

Append execution history where appropriate.

Keep logs concise and evidence-based.

Do not record credentials, tokens, API keys, session secrets, customer data or sensitive environment values.

## 3. HANDOFF FROM PREVIOUS AGENT

Before making changes:

1. Read existing `AGENTS.md` and `PROJECT_RULES.md`, if present.
2. Read `ui_modernization_logs/EXECUTION_CHECKPOINT.md`, if present.
3. Read the existing modernization completion and defect reports.
4. Inspect Git working-tree status.
5. Identify files modified by the previous execution.
6. Identify completed, incomplete and blocked work.
7. Verify that no other agent is actively modifying the same files.
8. Record the current baseline.

Do not reset, stash, discard, overwrite or revert uncommitted work without explicit approval.

Do not repeat previously completed work unless verification demonstrates a defect.

Create a concise handoff report.

## 4. TOOL REQUIREMENTS

Discover and use the following existing tools when available.

### Unslop

Use Unslop to audit and improve:

- UI consistency
- Component quality
- Readability
- Navigation
- Interaction design
- Responsive layouts
- Error presentation
- Accessibility
- Generic or low-quality AI-generated design patterns

Do not use Unslop to perform unrelated rewrites.

### Graphify

Use Graphify for targeted dependency and relationship analysis:

- Frontend-to-backend connections
- API routes
- Service dependencies
- Data flows
- Model inference paths
- Authentication dependencies
- Feature integration impact

### Archify

Use Archify to assess:

- Existing architecture
- Component reuse
- Service boundaries
- Integration architecture
- Technical dependencies
- Architectural risks

### Missing tools

If any tool is unavailable:

1. Search existing agent/MCP configuration.
2. Check existing installations.
3. Identify the exact intended package and trusted source.
4. Verify compatibility and security implications.
5. Propose installation if needed.
6. Obtain approval before installing or executing new third-party tools.
7. Continue using existing tools when installation is not approved.

Do not fabricate tool usage.

Record actual availability and execution evidence.

## 5. STRICT TOKEN-EFFICIENCY RULES

Apply these rules throughout execution:

- Search filenames before reading files.
- Search symbols and imports before opening modules.
- Read only relevant sections.
- Reuse previous architecture findings.
- Avoid scanning the entire repository repeatedly.
- Do not repeatedly inspect unchanged files.
- Use existing packages and components.
- Avoid duplicate implementations.
- Prefer targeted code modifications.
- Avoid unnecessary abstraction layers.
- Do not generate excessive documentation.
- Keep execution summaries short.
- Do not repeat completed tests without a reason.
- Run targeted tests before broad regression tests.
- Cache and reuse valid findings.
- Update checkpoints rather than recreating plans.

Do not compromise quality or security to save tokens.

## 6. EXISTING TECHNOLOGY PRESERVATION

Discover the actual technology stack before implementation.

Preserve the current:

- Python runtime
- FastAPI architecture
- Existing frontend technology
- Model packages
- Authentication approach
- Data persistence approach
- Docker configuration
- Application port 7005

Reuse existing dependencies whenever possible.

Do not introduce React, Next.js, new databases, Redis, Celery, MLflow, LangGraph, vector databases or cloud infrastructure unless an existing feature genuinely requires them and the change is separately approved.

No unnecessary framework migrations.

No unapproved dependency installations.

No unapproved database schema changes.

## 7. FEATURE-WISE FULL-STACK AUDIT AND REMEDIATION

For every module:

1. Identify existing UI controls.
2. Identify backend routes.
3. Identify service implementation.
4. Identify data sources.
5. Identify persistence behavior.
6. Identify actual ML/LLM integrations.
7. Identify authentication and authorization requirements.
8. Trace the complete user workflow.
9. Test successful scenarios.
10. Test failure scenarios.
11. Identify defects and missing integration.
12. Implement minimal fixes.
13. Retest affected functionality.
14. Record evidence.

Do not assume a feature works because its page loads.

Do not assume a feature is missing because its implementation is not immediately obvious.

### 7.1 Executive Overview

Ensure the dashboard correctly reflects available operational information.

Validate:

- Model inventory
- Fraud scoring activity
- Drift monitoring status
- Credit risk activity
- AML case summary
- LLMOps availability
- Recent events
- Application health

Use actual application data.

If metrics are unavailable, display honest empty states.

Do not invent transaction counts, model accuracy or monitoring statistics.

### 7.2 Fraud Scoring

Verify the complete transaction scoring workflow:

Transaction input → validation → preprocessing → model inference → result → explanation → authorized persistence/audit.

Test:

- Valid transactions
- Invalid amounts
- Missing fields
- Boundary conditions
- Model unavailable
- Repeated requests
- Unauthorized access
- Explanation consistency

Determine whether the existing implementation uses a trained model, heuristic or synthetic simulation.

Label the methodology accurately.

Do not present heuristic scores as calibrated fraud probabilities.

Preserve existing inference behavior unless a verified defect requires correction.

### 7.3 Model Registry

Verify:

- Model discovery
- Model metadata
- Version information
- Model artifact references
- Available evaluation metrics
- Lifecycle states
- Model loading
- Existing governance operations
- Authorization
- Audit logging

Do not fabricate model versions or performance metrics.

If model registration or promotion is already supported, test the actual lifecycle.

If unsupported, document the limitation rather than implementing a fake workflow.

### 7.4 Drift Monitoring

Validate:

- Baseline dataset availability
- Current dataset availability
- Feature compatibility
- Drift calculations
- Threshold handling
- Alert generation where supported
- Result persistence
- Historical results where supported

Use actual calculations.

Separate real monitoring from synthetic educational experiments.

Test missing baseline data and incompatible feature schemas.

Do not claim continuous monitoring unless scheduled execution actually exists.

### 7.5 Credit Risk

Verify the complete assessment workflow.

Validate:

- Annual income
- Debt
- Credit utilization
- Delinquencies
- Employment history
- Input constraints
- Backend calculations
- Risk index
- Risk classification
- Explanation
- Error handling

Ensure the frontend result matches the backend output.

Retain the educational disclaimer.

The existing heuristic must not be represented as a trained probability-of-default model.

Do not use it for real lending decisions.

### 7.6 AML & Cases

Verify:

- Case creation
- Case identifiers
- Case retrieval
- Case status
- Severity
- Investigation notes where supported
- Case updates
- Authorized actions
- Audit trail
- Persistence
- Error handling

Test invalid transitions and unauthorized actions.

Do not fabricate regulatory submissions, suspicious activity reports or compliance approvals.

### 7.7 LLMOps

Audit the actual LLMOps implementation.

Verify existing support for:

- Provider configuration
- Model selection
- API-key handling
- Prompt execution
- Token usage
- Latency measurement
- Evaluation
- Trace visibility
- Error handling
- Audit logging

If BYOK is implemented, verify that keys are handled securely and never exposed in responses or logs.

Do not make external paid API calls without approval.

Use mocks only for isolated automated tests, and label them as mocks.

Do not claim a provider integration works without a successful authorized live integration test.

### 7.8 Learning Lab

The Learning Lab must be an actual educational workspace, not a static collection of descriptions.

Audit existing lessons and experiments.

For supported topics, verify:

- Learning objectives
- Theory
- Practical exercises
- Executable demonstrations
- Input and output visibility
- Model explanations
- Evaluation metrics
- Error handling
- Experiment isolation
- Clear distinction between simulated and real execution

Reuse existing application capabilities.

Do not introduce unrelated training infrastructure.

Preserve administrator-only access.

### 7.9 Admin Console

Verify actual administrative workflows:

- User listing
- User creation where supported
- Role assignment
- User status changes
- Application configuration
- Audit log visibility
- Operational settings
- Security controls

Test administrator and non-administrator access.

Protect backend endpoints independently of frontend navigation.

Do not expose secrets or password hashes.

Do not create undocumented privileged accounts.

## 8. API AND DATA INTEGRITY

Audit frontend/backend integration.

For every existing interactive feature:

- Identify the endpoint.
- Verify HTTP method.
- Verify request schema.
- Verify response schema.
- Verify validation.
- Verify authentication.
- Verify authorization.
- Verify error handling.
- Verify persistence where expected.

Check for:

- Broken routes
- Incorrect payloads
- Missing error messages
- Unhandled exceptions
- Inconsistent response fields
- Duplicate records
- Incorrect state transitions
- Missing audit events
- Data leakage between roles

Use existing Pydantic schemas and service conventions.

Avoid unnecessary API redesign.

## 9. DATABASE AND PERSISTENCE

Identify the current storage mechanism.

Verify:

- Data creation
- Data retrieval
- Data updates
- Persistence across application restarts where applicable
- Referential consistency
- Input validation
- Failure handling

Use non-destructive tests and synthetic records.

Do not delete existing user data.

Do not run destructive migration commands.

Do not modify database schemas without approval.

If persistence requires schema changes, document the exact migration proposal and stop that change pending approval.

## 10. SECURITY AND RBAC

Verify:

- Login
- Logout
- Session handling
- Password security
- Protected endpoints
- Administrator-only modules
- Role restrictions
- Input validation
- Sensitive configuration protection
- Audit logging
- Error information exposure

Learning Lab and Admin Console must be administrator-only.

Use negative authorization tests.

A hidden navigation tab is not sufficient evidence of access control.

Do not perform destructive security testing.

Do not expose secrets in test evidence.

## 11. OBSERVABILITY

Improve observability using existing libraries and infrastructure.

Where appropriate:

- Structured application logs
- Request correlation identifiers
- Meaningful error messages
- Existing audit events
- Model execution timing
- Actual inference outcomes
- Available health indicators

Never log:

- Passwords
- Session secrets
- API keys
- Authorization headers
- Sensitive financial records

Do not install a large monitoring stack solely for this exercise.

## 12. UI AND UX CONTINUATION

Preserve the previous agent's modernization work.

Apply the established design system across all nine modules.

Verify:

- Sidebar navigation
- Header
- Page layouts
- Cards
- Tables
- Forms
- Modals
- Charts
- Validation messages
- Empty states
- Loading indicators
- Responsive behavior
- Accessibility basics

Every visual control must have a genuine function.

Remove or clearly disable nonfunctional controls.

Do not create decorative buttons that imply nonexistent capabilities.

Do not display raw JSON as the only result where a user-friendly presentation is appropriate.

Retain technical JSON views where useful for learning.

## 13. TEST DATA POLICY

Use synthetic data for testing.

Do not use real banking customer information.

Separate test data from existing application data where possible.

Tag created test records clearly.

Do not delete existing records.

Do not clean or reset databases without approval.

For tests that modify persistent data, record what was created.

Avoid creating excessive duplicate test records.

## 14. TESTING STRATEGY

### Layer 1 — Static checks

Run relevant:

- Python syntax checks
- Existing linting
- Existing type checks
- Existing frontend checks

### Layer 2 — Unit tests

Test affected business logic and validation.

### Layer 3 — API integration tests

Test actual API behavior using an isolated test environment.

### Layer 4 — Feature workflows

Test each feature's successful and unsuccessful paths.

### Layer 5 — RBAC tests

Test authorized and unauthorized access.

### Layer 6 — Browser testing

Use existing Playwright or other installed browser automation when available.

Verify navigation, forms, results, responsive layouts and visible errors.

### Layer 7 — Regression

Run broader regression tests once after integrated changes are ready, where feasible.

Do not repeatedly execute the full suite after every minor change.

### Test reporting

For every test record:

- Test ID
- Feature
- Scenario
- Expected outcome
- Actual outcome
- Execution method
- Result
- Evidence reference

Statuses:

PASS / FAIL / BLOCKED / NOT TESTED

Never fabricate test results.

## 15. DOCKER PROTECTION

Existing unrelated Docker applications are protected.

Do not:

- Stop unrelated containers
- Restart unrelated containers
- Remove unrelated images
- Delete volumes
- Modify shared networks
- Run Docker prune commands
- Run `docker compose down`
- Change unrelated host ports
- Modify other project directories

Preserve AWS_BANK port 7005.

Preserve the existing offline Python wheel installation strategy.

Do not download dependencies unnecessarily.

Do not rebuild AWS_BANK after every code change.

Perform source-level verification first.

**Do not rebuild, recreate or restart the running AWS_BANK container without explicit user approval.**

If deployment is not approved, complete all safe source-level work and report runtime verification as pending.

## 16. CHECKPOINT AND RESUME CONTROL

Maintain:

`enterprise_enhancement_logs/EXECUTION_CHECKPOINT.md`

After every completed feature or meaningful execution phase, record:

- Timestamp
- Current phase
- Completed tasks
- Pending tasks
- Modified files
- Tests executed
- Verified results
- Defects
- Blockers
- Next action

When execution resumes:

1. Read the checkpoint.
2. Inspect the working tree.
3. Identify incomplete tasks.
4. Reuse previous findings.
5. Resume from the last verified state.
6. Avoid repeating completed work.

Never declare completion simply because a checkpoint says a task was attempted.

## 17. DEFECT REMEDIATION

Create a feature-specific defect record for each verified issue.

Use:

`enterprise_enhancement_logs/defects/`

Include:

- Defect ID
- Severity
- Reproduction steps
- Expected behavior
- Actual behavior
- Root cause
- Affected files
- Fix
- Test evidence
- Final status

Prioritize:

P0 — Security or data integrity critical issue

P1 — Core workflow broken

P2 — Partial functionality or significant usability defect

P3 — Cosmetic or minor issue

Fix P0/P1 defects first.

Do not introduce unrelated improvements while resolving a defect.

## 18. IMPLEMENTATION ORDER

Execute in controlled phases.

**Phase A — Handoff and discovery**

Read previous logs, inspect the existing architecture, identify available tools and create the baseline.

**Phase B — Full-stack gap assessment**

Audit all nine modules and classify gaps.

**Phase C — Critical remediation**

Fix confirmed security, authentication, persistence and core API defects within authorized boundaries.

**Phase D — Feature integration**

Complete existing feature workflows one module at a time.

**Phase E — UI integration**

Ensure modernized screens work with actual backend services.

**Phase F — MLOps and LLMOps verification**

Verify real model execution, monitoring and existing integrations.

**Phase G — End-to-end testing**

Execute feature-level, integration, security and regression tests.

**Phase H — Final acceptance**

Produce a complete evidence-based assessment.

Do not start a later phase merely because an earlier phase has been documented. Complete the authorized work and verify it.

## 19. STOP CONDITIONS

Stop the affected operation and request approval if it requires:

- Database schema migration
- Destructive data changes
- New paid services
- New cloud resources
- New external API spending
- Unapproved third-party installations
- Framework migration
- Changes to authentication architecture
- Docker container recreation
- Restarting running services
- Changes outside AWS_BANK
- Access to unavailable credentials

Continue independent safe tasks where possible.

Document blockers.

Do not silently bypass restrictions.

## 20. COMPLETION REQUIREMENTS

A module can be marked PASS only if:

1. Its UI is functional.
2. Its backend integration works.
3. Its existing business logic executes correctly.
4. Its data behavior is verified where applicable.
5. Its access controls are verified.
6. Its error handling is tested.
7. Its relevant tests pass.
8. Evidence is recorded.

A feature cannot be marked PASS based only on code inspection, generated code or screenshots.

If deployment is pending, distinguish source-level verification from deployed runtime verification.

Do not claim the entire application is production-ready merely because the learning demonstration works.

## 21. FINAL DELIVERABLES

Produce:

1. Full-stack gap assessment
2. Modernized integrated application source
3. Feature-wise implementation logs
4. API validation results
5. MLOps validation results
6. LLMOps validation results
7. Security/RBAC test results
8. End-to-end functional test results
9. Defect tracker
10. Updated execution checkpoint
11. Controlled deployment plan
12. Final acceptance report

The final report must include a feature matrix showing:

- UI status
- Backend status
- Integration status
- Test status
- Known limitations
- Evidence references

Use PASS, PARTIAL, FAIL, BLOCKED or NOT TESTED accurately.

## 22. FINAL EXECUTION INSTRUCTION

Start by reading the existing AWS_BANK UI modernization checkpoint and current Git status.

Do not repeat completed modernization work.

Discover and use Unslop, Graphify and Archify where available.

Perform a bounded full-stack audit.

Fix verified issues using existing packages and architecture.

Complete the nine existing application modules within approved scope.

Preserve all previous work and test evidence.

Minimize unnecessary token consumption.

Do not stop after generating plans or reports.

Continue implementation and targeted verification until the authorized work is complete or a genuine blocker requires user approval.

Never fabricate execution results, model predictions, screenshots, tool usage or completion status.

**The objective is a genuinely functional, integrated AWS_BANK enterprise AI/MLOps showcase—not merely a visually improved dashboard.**