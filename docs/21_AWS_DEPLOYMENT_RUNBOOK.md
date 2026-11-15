# AWS deployment runbook — provisioned design, NOT executed

## Deployment decision

Amazon Bedrock is optional model inference, not application hosting. The target is ECR → ECS Fargate in private subnets → HTTPS ALB/WAF → RDS PostgreSQL, with S3 model artifacts, Secrets Manager, KMS, CloudWatch, IAM and Budgets. Existing SQLite/joblib local persistence must not be used by horizontally scaled ECS tasks.

## Required placeholders

Record these in an approved deployment change, never in source control:

```text
AWS_ACCOUNT_ID=<approved account>
AWS_REGION=<approved region>
ECR_REPOSITORY=<repository name>
ECS_CLUSTER=<cluster name>
ECS_SERVICE=<service name>
ALB_DNS=<validated HTTPS endpoint>
RDS_ENDPOINT=<private endpoint>
S3_BUCKET=<encrypted artifact bucket>
SECRET_ARN=<Secrets Manager secret>
TASK_ROLE_ARN=<least-privilege runtime role>
DEPLOY_ROLE_ARN=<restricted CI/CD role>
```

## Preconditions and gates

1. Obtain written account, region, cost, data-residency and deployment approval; require MFA and a short-lived deploy role.
2. Complete the migration design from SQLite to PostgreSQL, including additive schema mapping, backfill validation, rollback, and restore rehearsal. Do not point multiple tasks at SQLite.
3. Add a configurable artifact store abstraction. Upload signed, versioned joblib/model metadata to encrypted S3; verify checksum before loading.
4. Review IAM policies for ECR pull, S3 prefix access, Secrets Manager read, CloudWatch logs and optional Bedrock invoke. Deny wildcard write and public bucket access.
5. Review Terraform plan for VPC/private subnets, security groups, NAT/VPC endpoints, ALB certificate, WAF, RDS, S3, KMS, alarms and Budgets. Do not apply without approval.

## Build and release sequence (commands are examples; not executed)

1. Run dependency audit, Python compile, focused banking tests, full tests, Auto Evals and security checks.
2. Build the pinned image and scan it with the approved image scanner.
3. Push an immutable image tag to ECR; never deploy `latest` as the release identifier.
4. Run database migration as a one-shot controlled job; record row counts, checksums and rollback checkpoint.
5. Deploy one canary ECS task with 1–2 healthy tasks required before traffic shift. Configure ALB health path `/api/health`, timeout, retries and deregistration delay.
6. Verify login/RBAC, account ownership, atomic transfer replay, statements, model scoring, failed quality-gate promotion, audit events and RAG abstention using synthetic data.
7. Shift traffic gradually only after logs, latency, CPU, memory, OOM and error-rate gates pass.

## Observability and security checks

- ALB access logs, ECS application logs and audit events go to retained, access-controlled CloudWatch destinations.
- Alarms cover 5xx rate, latency, unhealthy tasks, restart count, OOM, RDS storage/CPU/connections, failed logins and unusual transfer failures.
- Enforce HTTPS, secure cookies, CSRF strategy, SSO/MFA, WAF rules, private database access, encryption at rest/in transit, secret rotation and least privilege.
- Do not send customer or production banking data to Bedrock without approved governance, redaction and retention policy.

## Rollback and recovery

1. Stop traffic shift and restore the previous immutable ECS task definition/image.
2. Roll back application migrations only through a reviewed reversible migration; restore RDS from a tested point-in-time or snapshot path when required.
3. Restore model artifacts by version/checksum from S3 and re-check registry/evaluation evidence before scoring.
4. Preserve CloudWatch/audit evidence and open an incident record. Do not delete the failed deployment for forensic reasons.

## Cost and cleanup

Set Budgets alerts before provisioning. Estimate Fargate tasks, ALB, NAT/VPC endpoints, RDS tier, S3, logs, WAF and optional Bedrock tokens. Cleanup is a reviewed change: drain service, retain required logs/backups, remove only approved resources, and confirm no orphaned load balancers, IPs, snapshots or buckets.

No AWS resources, credentials or cloud commands were used for this repository validation.
