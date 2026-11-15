# Terraform implementation boundary

This directory is reserved for reviewed AWS infrastructure-as-code. No deployable Terraform resources are shipped because the current application uses local SQLite and joblib artifacts; deploying it directly would risk data loss and insecure operation. Required implementation: VPC, ECS/Fargate, ALB, ECR, RDS PostgreSQL, S3, KMS, Secrets Manager, CloudWatch, IAM, security groups, budgets and rollback. See docs/21_AWS_DEPLOYMENT_RUNBOOK.md.
