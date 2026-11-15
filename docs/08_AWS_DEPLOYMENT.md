# AWS deployment plan (future; not deployed)

## Critical distinction
Amazon Bedrock is an LLM inference service, **not a Docker application hosting platform**. Host AWS_BANK on ECS Fargate (preferred for production), with Bedrock as an optional AI analysis provider. For small nonproduction demos consider Lightsail/EC2 after comparing costs and security requirements.

## Production-ready topology
ECR image → ECS Fargate private subnets → ALB HTTPS + WAF → RDS PostgreSQL for metadata → S3 encrypted artifacts → CloudWatch logs/metrics → Secrets Manager + IAM task role. Separate MLflow tracking server and registry when needed. Optional Bedrock calls via IAM and private endpoints if supported. Restrict network egress and use AWS Budgets (alerts do not enforce a hard cap).

## Deployment steps
1. Create AWS account budget alerts, IAM least privilege, isolated VPC, ECR repository, KMS keys and Secrets Manager secrets.
2. Replace SQLite with PostgreSQL using Alembic migrations and automated backup tests. Replace local model artifacts with signed, versioned S3 artifacts. **Do not deploy multiple tasks against local SQLite.**
3. Add TLS, CSRF, MFA/SSO, rate limiting, secure cookies, audit retention and artifact integrity checks.
4. Build and scan image; push to ECR using CI OIDC, not static access keys.
5. Deploy ECS Fargate task with compatible CPU/memory configuration, ALB health checks, log driver and auto scaling. Benchmark memory under peak training; run training as separate ECS task if needed.
6. Validate rollback, DB restore, model recovery, CloudWatch alerts, data residency, secret rotation and incident runbook.
7. Only then enable Bedrock inference gateway with IAM policy, guardrails, PII policy, model allowlist, cost limits and prompt evaluation.

## Infrastructure files
`infra/aws-architecture.md` is a design blueprint, **not runnable Terraform**. Do not represent the cloud path as one-click ready until infrastructure, migrations, security controls and tests exist.
