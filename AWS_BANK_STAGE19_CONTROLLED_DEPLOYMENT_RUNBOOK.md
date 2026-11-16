# AWS_BANK — Stage 19 Controlled Deployment Runbook

**Status:** PREPARATION ONLY. **No approval to apply or provision.**

## Baseline and hard boundaries

- Repository: `C:\Users\raj45\OneDrive\Desktop\AWS_BANK_project\AWS_BANK_git_sync`
- Terraform: `infra\aws`; AWS account `213473482400`; region `ap-southeast-2`.
- Expected EC2: one `t3.small`; no inbound security-group rules; IMDSv2 required; encrypted root and 30-GiB data EBS.
- Expected image: immutable digest `sha256:911cbbb3e2156aea92ca34a2edbb9d2451435194db3213dbfcf16e2b2995241b` in account ECR.
- Stage 18 plan (refresh disabled): 22 adds / 0 changes / 0 destroys. **Not authorized for application.**
- Protect original AWS_BANK source, all unrelated Docker containers, Terraform state, and secrets. Never log decrypted parameters, user-data containing secrets, credentials, or unredacted plan JSON.
- `$50` AWS Budget is **alerts only**, not a cap. EBS, ECR, public IPv4, logs, and backend storage can accrue charges when EC2 is stopped.

## Checkpoint A — Read-only preflight (safe to run now)

Run the accompanying `AWS_BANK_STAGE19_PREFLIGHT.ps1`. It checks identity, repo status, Terraform formatting/validation, and generates a **fresh normal-refresh plan** to a local protected path. `terraform plan` can perform remote *read* requests but does not apply resources; backend locking may create a transient state lock. If strictly no remote write of any kind is allowed, omit the plan step and use the previously inspected Stage 18 plan only as historical evidence.

**Gate A:** Account must be `213473482400`; region must be explicit `ap-southeast-2`; Terraform validates; no unexpected actions. Investigate any discrepancies. Do not use an old plan for apply. Plan files may contain secrets; do not commit or upload them.

## Checkpoint B — Manual plan review and approval (future)

Inspect the plan locally with `terraform show -no-color <plan-path>` and `terraform show -json <plan-path>` **without publishing the output**. Check each IAM policy, EC2 AMI/type, encrypted volumes, security groups, SSM parameter references, ECR digest, CloudWatch, AWS Budget, public IPv4 and all billable resources. Validate expected counts (22/0/0) against *current* state, not as an unconditional requirement. A new refreshed plan can differ legitimately; differences require explicit review.

**Gate B:** Record plan SHA-256, creation time, AWS account, region, Terraform workspace, reviewer and approval. Stop on deletions/replacements, unexpected additions or IAM expansion. **Ask user for separate explicit authorization to provision and incur charges.**

## Checkpoint C — Provisioning (DOCUMENTATION ONLY — DO NOT EXECUTE)

Only after the user separately approves the **specific fresh plan**, an operator may execute in `infra\aws`:

```powershell
# FUTURE ONLY — NOT AUTHORIZED IN STAGE 19 PREPARATION
# terraform apply -input=false "<absolute-path-to-approved-fresh-plan.tfplan>"
```

A saved plan must be applied unmodified, from the same initialized backend/workspace. Do not use `-auto-approve` or generate a new plan silently. Capture exit code and nonsecret resource IDs. Do not run a second apply after a partial failure until inspecting state and actual resources.

**Gate C:** Terraform exit success and resources present as expected; otherwise stop and assess, without automatic destroy.

## Checkpoint D — Runtime validation (FUTURE ONLY)

1. **SSM readiness:** `aws ssm describe-instance-information --region ap-southeast-2` and confirm the deployed instance appears Online. If not, check instance profile, SSM Agent, network outbound/DNS, and CloudWatch logs. Do not open inbound SSH.
2. **ECR/bootstrap:** Via an explicitly approved SSM session, inspect `systemctl status` for the named application service and Docker, `docker ps`, and redacted journal logs. Confirm image **digest**, container health, and correct encrypted data mount (`lsblk -f`, `findmnt`). Do not print secret environment variables or parameter values.
3. **Synthetic banking:** Test login, authorized account views, transfers with synthetic data, and audit trails; no real customer data or external payments.
4. **RBAC:** Confirm regular users cannot access admin console, AI configuration, MLOps/LLMOps, or model governance endpoints. Confirm admin can access authorized controls. Record denied requests without tokens.
5. **IAM negative authorization:** First use a documented policy simulation or safe dry-run with the deployed role context where supported. **Never invoke a real StopInstances call against another instance.** Verify that the same-role/different-instance target is denied; distinguish simulated from live evidence.
6. **EBS persistence:** Record a synthetic marker on the data volume, reboot the approved EC2 instance in a scheduled window, confirm the same volume is mounted and marker remains. Do not detach, reformat, or delete volumes.
7. **Shutdown:** Test timer service status and logs. Validate extension using its documented root-only interface. A short-duration test may be used **only after separately approved code/config changes**; do not modify live timer silently. Confirm automatic stop after four hours, then verify recovery on next approved start. Verify the instance stops rather than terminates.
8. **Costs:** Verify EC2 state, EBS volumes, public IPv4 allocation, CloudWatch ingestion, and Budget alert. Record accrued/estimated costs; budget notifications do not hard-stop spending.

**Gate D:** Each item PASS/FAIL/PENDING with timestamps, redacted evidence and instance ID. Any failure blocks production/learning acceptance; don't claim complete until observed.

## Checkpoint E — Incident and rollback policy

- Unexpected plan or account: **stop before apply**.
- Partial apply: capture Terraform state/IDs and AWS evidence; reconcile manually. Do not destroy by default.
- Bootstrap failure: leave instance isolated (zero inbound), inspect SSM and redacted logs; stop compute if necessary **only with approval**. Preserve EBS.
- Unexpected spending: explicitly approve EC2 stop and subsequent cost remediation; stopping compute does not remove EBS/public IPv4/storage charges.
- IAM test failure: block acceptance and correct policy via a separately reviewed plan; never broaden IAM as a quick workaround.
- Data recovery: preserve volume and snapshots, verify actual attachment and encryption; no automated format or deletion.

## Required execution records

Store under `deployment_logs/stage19_deployment/` (when authorized): `00_APPROVAL.md`, `01_PREFLIGHT.md`, `02_FRESH_PLAN_REVIEW.md`, `03_APPLY_RESULT.md`, `04_SSM_BOOT_HEALTH.md`, `05_BANKING_RBAC.md`, `06_IAM_NEGATIVE_TEST.md`, `07_EBS_REBOOT.md`, `08_SHUTDOWN_EXTENSION.md`, `09_COSTS.md`, `10_FINAL_GO_NO_GO.md`, `EXECUTION_CHECKPOINT.json`. Redact all secrets, protect plan files, and use `PENDING` rather than guessing.

**Current decision:** READY FOR A SEPARATE DEPLOYMENT APPROVAL REVIEW; **NO APPLY AUTHORIZED**.
