# AWS_BANK — Enterprise UI Modernization Master Execution Prompt

## 1. Mission

Transform the existing AWS_BANK MLOps Control Center into a professional, modern, enterprise-grade banking AI and MLOps showcase.

The application must be suitable for:

- AI Architect interviews
- MLOps demonstrations
- Banking AI architecture demonstrations
- Technical learning
- Enterprise portfolio presentations

Modernize the complete application without breaking existing functionality.

**Primary principle: Improve the existing application, not rebuild it unnecessarily.**

Preserve all working business logic, authentication, API contracts, data, models, configurations and Docker infrastructure.

## 2. Strict scope and boundaries

Project root:

`C:\Users\raj45\OneDrive\Desktop\AWS_BANK_project\AWS_BANK_enterprise_v1\AWS_BANK`

Authorized scope:

- AWS_BANK frontend UI and UX
- Existing frontend components and styling
- Feature-level usability improvements
- Accessibility and responsiveness
- UI integration fixes directly caused by modernization
- Relevant tests and documentation

Out of scope without explicit approval:

- Replacing the frontend framework
- Backend architectural redesign
- Database migrations
- ML model retraining
- Changing scoring algorithms
- Replacing authentication
- Introducing paid services
- Modifying unrelated applications
- Changing Docker networking or ports
- Installing unnecessary dependencies

If a requested enhancement requires an out-of-scope change, document it and request approval rather than expanding scope independently.

## 3. Mandatory tool discovery — Unslop, Graphify and Archify

Before implementation, inspect the current environment.

### Unslop

Use the existing Unslop tool or workflow, if available, to improve UI quality and remove generic AI-generated design patterns.

Review:

- Visual hierarchy
- Typography
- Spacing
- Component consistency
- Navigation
- Accessibility
- Layout quality
- Responsive behavior
- Unnecessary decoration
- Poorly designed forms and buttons

Apply findings selectively. Preserve application functionality.

### Graphify

Discover whether Graphify is available through:

- Existing agent tools or MCP servers
- Project configuration
- Installed CLI tools
- Existing local repositories

If available, use it to understand:

- Component relationships
- Route dependencies
- API interactions
- Relevant module connections
- Potential regression impact

Do not graph the entire repository unless necessary.

### Archify

Discover whether Archify is available through the same approved mechanisms.

If available, use it to:

- Understand the current architecture
- Identify reusable components
- Identify existing frontend conventions
- Locate relevant services
- Assess architectural impact
- Prevent duplicate implementations

### If tools are missing

1. Check existing installations and configuration.
2. Identify the exact intended tool, publisher, repository and compatible version.
3. Prefer an existing trusted installation or already-approved package.
4. If installation is required, create a short installation proposal containing source, version, permissions, dependencies, security implications and expected benefit.
5. Request approval before installing or executing newly obtained third-party code.
6. If approval is unavailable, continue with built-in repository search and static analysis.
7. Mark unavailable tools as UNAVAILABLE rather than claiming they were used.

Never invent tool output or claim a tool was executed when it was not.

Record findings in:

`ui_modernization_logs/01_TOOL_DISCOVERY.md`

## 4. Mandatory token-efficiency rules

Minimize token consumption without compromising implementation quality.

### Repository exploration

- Search filenames before opening files.
- Search symbols, routes, imports and components first.
- Read only relevant file sections.
- Do not repeatedly read unchanged files.
- Do not dump large files unnecessarily.
- Avoid full-repository scans.
- Reuse previously collected architecture information.
- Use Graphify or Archify results to narrow inspection when available.

### Implementation

- Make small, targeted changes.
- Reuse existing components.
- Reuse installed packages.
- Reuse existing CSS and UI conventions where appropriate.
- Avoid duplicate utilities.
- Avoid unnecessary abstraction layers.
- Avoid broad refactoring.
- Do not rewrite working code for cosmetic reasons.
- Do not migrate frameworks without approval.

### Testing

- Test affected functionality first.
- Run targeted linting and type checks.
- Avoid repeated full builds.
- Do not rerun unchanged passing tests without reason.
- Expand regression testing only when justified.
- Record test evidence once and reuse it.

### Agent communication

- Keep progress messages concise.
- Avoid repeating completed findings.
- Do not produce lengthy explanations during execution.
- Maintain concise checkpoint summaries.
- Report blockers immediately.
- Do not repeatedly ask questions already answered by project configuration.

Token optimization must never justify skipping required security checks or falsely declaring success.

## 5. Existing package reuse

Before adding any dependency:

1. Inspect existing package manifests and installed dependencies.
2. Check whether the required functionality already exists.
3. Prefer native browser capabilities where suitable.
4. Reuse current styling and UI libraries.
5. Avoid introducing overlapping component libraries.
6. Evaluate bundle size, maintenance and security.
7. Obtain approval before installing a new dependency.

Do not introduce React, Tailwind, shadcn/ui or another framework solely for visual modernization.

Use the existing architecture unless a migration is separately approved.

## 6. Enterprise visual design system

Create a consistent corporate design system.

### Visual identity

Use a balanced palette:

- Deep navy for primary navigation and headings
- Purple/violet for brand identity
- Blue for primary interactive actions
- Teal for successful operations
- Amber for warnings
- Red for critical alerts
- Neutral white and gray surfaces

Use appropriate colors according to meaning.

Avoid making every element purple.

### Typography

- Professional, readable fonts
- Clear heading hierarchy
- Comfortable body text
- Consistent font sizes
- Readable labels
- Appropriate contrast
- Responsive typography

### Icons

Use existing icon packages where possible.

Prefer recognizable enterprise icons.

Avoid:

- Random decorative symbols
- Emoji-based navigation
- Excessively futuristic AI icons
- Inconsistent icon styles
- Unnecessary icon duplication

### Layout

Implement:

- Collapsible left sidebar
- Professional application header
- User profile area
- Active navigation indicators
- Consistent content width
- Responsive grid layouts
- Reusable cards
- Standardized forms
- Tables and filters
- Contextual help
- Empty, loading and error states

Preserve keyboard accessibility and mobile navigation.

## 7. Modernize every existing feature

### 7.1 Executive Overview

Create an enterprise dashboard featuring:

- Model inventory summary
- Fraud scoring activity
- Model monitoring status
- Drift alerts
- Credit risk activity
- AML case activity
- System health
- Recent operational events

Use real backend data where available.

If data is unavailable, show a clear empty state.

Never invent live metrics.

### 7.2 Fraud Scoring

Improve:

- Transaction entry
- Input validation
- Fraud assessment presentation
- Model explanation
- Risk visualization
- Assessment details
- Error handling

Preserve existing scoring logic.

### 7.3 Model Registry

Improve:

- Model listing
- Version information
- Lifecycle indicators
- Model details
- Evaluation metrics
- Available governance actions

Do not add fake model deployment functionality.

### 7.4 Drift Monitoring

Improve:

- Drift indicators
- Feature comparisons
- Monitoring thresholds
- Baseline/current comparisons
- Historical visualization where supported
- Alert presentation

Distinguish synthetic and real monitoring data.

### 7.5 Credit Risk

Replace raw JSON-only output with:

- Professional input form
- Assessment summary
- Risk index visualization
- Explanation panel
- Validated contributing factors
- Collapsible technical JSON
- Clear educational disclaimer

Preserve the existing heuristic model and scoring behavior.

Do not present the heuristic as a calibrated probability of default.

### 7.6 AML & Cases

Improve:

- Case listing
- Severity indicators
- Case details
- Investigation workflow
- Status visualization
- Evidence display
- Existing audit information

Preserve actual workflow rules.

### 7.7 LLMOps

Improve:

- Provider configuration interface
- Model information
- Prompt evaluation workspace
- Available metrics
- Trace presentation
- Error states
- Technical details

Do not fabricate model responses or metrics.

### 7.8 Learning Lab

Build a professional administrator-only educational workspace.

Include existing supported learning workflows with:

- Clear concept explanations
- Guided experiments
- Architecture illustrations where appropriate
- Model evaluation explanations
- Practical learning steps
- Technical references
- Real versus simulated execution labels

Do not replace working educational content with decorative placeholders.

### 7.9 Admin Console

Improve:

- User management
- Role visibility
- Security settings
- Application configuration
- Audit information
- Operational status

Preserve all existing backend authorization checks.

Admin Console and Learning Lab must remain restricted to authorized administrators.

## 8. Mandatory functional preservation

For every changed feature:

- Preserve routes.
- Preserve API contracts.
- Preserve authentication.
- Preserve role permissions.
- Preserve application data.
- Preserve model behavior.
- Preserve audit functionality.
- Preserve existing error handling.
- Preserve security controls.

Do not modify working backend logic merely to support a new appearance.

If backend changes are essential, document the dependency and obtain approval before proceeding.

## 9. Docker isolation and protection

AWS_BANK runs alongside other Docker applications.

### Protected resources

All unrelated:

- Containers
- Images
- Volumes
- Networks
- Databases
- Applications
- Host ports

### Prohibited operations

Do not execute:

- `docker system prune`
- `docker volume prune`
- `docker network prune`
- `docker compose down`
- Global container stop commands
- Global container removal commands
- Unrelated image deletion
- Unrelated network modifications

Do not change port 7005.

Do not restart or rebuild unrelated containers.

### AWS_BANK deployment

- Inspect existing Compose configuration.
- Preserve environment variables.
- Preserve application data.
- Preserve the offline wheel installation approach.
- Do not unnecessarily reinstall dependencies.
- Do not rebuild Docker after every UI change.
- Run source-level checks first.
- Obtain explicit approval before rebuilding or restarting the running AWS_BANK service.

If Docker access fails, record the blocker and continue with safe source-level tasks.

Never bypass Docker permissions or modify unrelated infrastructure.

## 10. Persistent logs and checkpoints

Create:

`AWS_BANK/ui_modernization_logs/`

Required structure:

```text
ui_modernization_logs/
├── 00_BASELINE.md
├── 01_TOOL_DISCOVERY.md
├── 02_ARCHITECTURE_ANALYSIS.md
├── 03_UI_AUDIT.md
├── 04_DESIGN_SYSTEM.md
├── 05_IMPLEMENTATION_PLAN.md
├── 06_FEATURE_PROGRESS.md
├── 07_TEST_RESULTS.md
├── 08_SECURITY_RBAC.md
├── 09_DEFECT_TRACKER.md
├── 10_FINAL_ACCEPTANCE.md
├── EXECUTION_CHECKPOINT.md
└── feature_logs/
```

### Log preservation

- Never delete previous logs.
- Never silently overwrite completed reports.
- Append dated execution entries where appropriate.
- Preserve historical findings.
- Maintain feature-specific records.
- Avoid duplicating identical findings across files.
- Store detailed evidence in feature logs.
- Keep global reports concise.
- Reference existing evidence instead of copying it repeatedly.

### Checkpoint requirements

Update `EXECUTION_CHECKPOINT.md` after each meaningful phase.

Include:

- Current phase
- Completed features
- Pending features
- Modified files
- Test status
- Known defects
- Blockers
- Next safe action
- Last verified state

### Resume behavior

At the start of a resumed session:

1. Read `EXECUTION_CHECKPOINT.md`.
2. Read only relevant unfinished feature logs.
3. Verify the current working tree.
4. Resume from the last verified checkpoint.
5. Do not repeat completed analysis or tests unnecessarily.
6. Do not overwrite newer work.

## 11. Defect management

For each defect, record:

- Unique defect ID
- Feature
- Severity
- Reproduction steps
- Expected behavior
- Actual behavior
- Root cause, if verified
- Modified files
- Fix status
- Verification evidence

Fix defects introduced by modernization.

For pre-existing unrelated defects, document them without expanding scope automatically.

## 12. Verification and acceptance

Every feature must pass relevant checks:

- Navigation
- Form behavior
- API integration
- Validation
- Authentication
- Authorization
- Error handling
- Responsive layout
- Accessibility basics
- Existing functionality regression

Use browser automation only when available and authorized.

Do not claim browser verification if no browser was used.

Do not claim a test passed without executing it.

Do not use fabricated screenshots or test output.

### Completion status

Use:

- PASS — implemented and verified
- PARTIAL — implemented but incompletely verified
- FAIL — verified failure
- BLOCKED — cannot proceed because of a documented blocker
- NOT TESTED — verification not performed

Never mark a feature PASS merely because its code was written.

## 13. Execution sequence

Follow this order:

1. Tool discovery
2. Architecture assessment
3. Existing UI audit
4. Design system
5. Application shell modernization
6. Executive Overview
7. Fraud Scoring
8. Model Registry
9. Drift Monitoring
10. Credit Risk
11. AML & Cases
12. LLMOps
13. Learning Lab
14. Admin Console
15. Targeted regression testing
16. Security and RBAC verification
17. Final acceptance report

Work incrementally.

Do not perform multiple unrelated large changes simultaneously.

Maintain checkpoints after each stage.

## 14. Strict completion rules

Do not declare success based on:

- Code generation alone
- A visually attractive screenshot
- A successful Docker build alone
- Passing lint alone
- Static mock data
- Unverified assumptions
- Agent-generated status messages

Completion requires actual implementation and relevant verification evidence.

If a tool is unavailable, disclose it.

If tests are blocked, disclose them.

If a feature is incomplete, disclose it.

If runtime deployment is not authorized, leave it pending.

## 15. Final output

Provide a concise report containing:

1. Features modernized
2. Existing functionality preserved
3. Tools actually used
4. Packages reused
5. New dependencies, if approved
6. Modified files
7. Tests executed
8. Security verification
9. Outstanding defects
10. Docker deployment status
11. Final PASS / PARTIAL / BLOCKED assessment

Do not provide repetitive summaries.

Do not consume additional tokens on unrelated improvements.

## 16. Start instruction

Begin with a bounded discovery of AWS_BANK.

First inspect project rules, current UI architecture, existing packages, Unslop availability, Graphify availability and Archify availability.

Create the baseline and execution checkpoint.

Then implement the modernization incrementally within the approved scope.

**Do not stop after producing a plan. Proceed with implementation where authorized, preserve checkpoints, and stop only for genuine blockers, required approvals or completed scope.**