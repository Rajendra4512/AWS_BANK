# Terraform state bootstrap — manual and separate

This repository intentionally does not create or initialize the Terraform state bucket. Bootstrap it once in the approved AWS account, using an operator session with a narrowly scoped bootstrap role. Do not run these commands from CI and do not place credentials in files or shell history.

The state bucket must be unique, in `ap-southeast-2`, private, versioned, encrypted, and protected from public access. Native S3 lockfiles require Terraform 1.10 or newer and `use_lockfile = true`; do not add a DynamoDB lock table for this design.

Example manual bootstrap commands, with placeholders replaced only by the approved operator:

```bash
export STATE_BUCKET='REPLACE_WITH_UNIQUE_STATE_BUCKET'
aws s3api create-bucket --bucket "$STATE_BUCKET" --region ap-southeast-2 --create-bucket-configuration LocationConstraint=ap-southeast-2
aws s3api put-public-access-block --bucket "$STATE_BUCKET" --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-versioning --bucket "$STATE_BUCKET" --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket "$STATE_BUCKET" --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

Review the bucket policy before applying it. The Terraform operator role needs `s3:ListBucket` on the bucket and `s3:GetObject`, `s3:PutObject`, and `s3:DeleteObject` only for `aws-bank/development/terraform.tfstate` and its `.tflock` object. A separate read-only recovery role should receive version-list/get access.

Copy `backend.tf.example` to a separately reviewed backend configuration, replace only the bucket placeholder, then run:

```bash
terraform init -backend-config=backend.tf.example
```

Do not run `-migrate-state` automatically. If a local state already exists, stop and review the state lineage and destination key first; initializing against the wrong bucket/key can create conflicting state and concurrent ownership. Record the selected account, bucket, key, lockfile behavior, and recovery version before any migration approval.

Recovery: list object versions, identify the last known-good state version, copy it to a quarantined recovery key, validate with `terraform plan -refresh-only`, and only then approve any state recovery. Never delete old state versions as routine cleanup.
