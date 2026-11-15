# AWS resource blueprint

Region: user-selected; default none to avoid accidental spend. Resources to provision after security gate: ECR, ECS cluster/service/task, private subnets, ALB+ACM, WAF, RDS PostgreSQL, S3 model artifacts, Secrets Manager, CloudWatch, IAM task execution + task roles, VPC endpoints where justified. Optional: separate MLflow server and Bedrock Runtime invocation permission. Use IaC with explicit approval and `plan` review; never auto-apply to unknown account. No AWS credentials in repo. Cost review required before provisioning.
