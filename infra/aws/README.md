# AWS_BANK offline AWS preparation

This Terraform is preparation only. It intentionally has no initialized backend and must not be run with `terraform apply` without a separately approved account, state, security, cost, certificate, and rollback review.

The initial design is a single CPU-only EC2 instance in Sydney (`ap-southeast-2`) and the `development` environment, with no inbound security-group rules, an encrypted EBS data volume for the current SQLite persistence boundary, private versioned/encrypted S3 model artifacts, immutable ECR tags, an EC2 instance role, CloudWatch logs/alarms, and an AWS Budget.

The AWS provider constraint is `~> 6.0`; the current official Registry documentation reports the 6.x provider family and must be pinned in a reviewed lock file before initialization.

## Required approvals and inputs

- AWS account activation and billing-owner approval.
- The application is private in this phase. Use SSM Session Manager port forwarding; do not expose 443 or 7005. A future HTTPS/domain/certificate design requires a separate approval.
- Approved SSM SecureString parameters for the bootstrap password and session secret.
- Approved OIDC role trust policy for the GitHub repository and production environment.
- An immutable ECR image URI containing the reviewed Git commit SHA or an image digest; empty image URIs are rejected by Terraform/bootstrap.
- Review of SQLite/EBS backup and restore; multi-instance scaling is not supported by the current schema/runtime.

## Safe offline checks

```powershell
terraform fmt -check -recursive infra/aws
terraform init -backend=false -input=false infra/aws
terraform validate infra/aws
```

`terraform init` may require provider download and is not an AWS resource operation; do not configure a remote backend or credentials during local review. If Terraform is unavailable, record the blocker rather than installing broadly.

## Operational boundaries

- No inbound ingress is defined; use `aws ssm start-session` port forwarding to access the private application.
- The public IP is retained only for outbound access because this no-NAT development subnet needs ECR/S3/SSM connectivity; it is not an inbound application path. A private subnet with VPC endpoints or NAT is a future cost/security decision.
- S3 artifacts are versioned and the application continues to verify SHA-256 manifests and fail closed.
- The bootstrap resolves the Terraform-provided EBS volume ID through Nitro device metadata, refuses ambiguous/partitioned devices, never reformats an existing filesystem, mounts by UUID, and gates Docker/systemd startup on the verified mount.
- `user_data_replace_on_change` is false to avoid unexpected EC2 replacement; use an approved SSM maintenance procedure for bootstrap changes.
- EC2 stop preserves the instance and EBS volumes; termination does not automatically imply volume deletion in this design. S3 artifacts remain until explicitly and separately reviewed.
- Terraform destroy is prohibited by the preparation task; retain state and backups according to an approved recovery plan.
