variable "aws_region" {
  type        = string
  description = "AWS region; Sydney is the initial development default."
  default     = "ap-southeast-2"
}

variable "project_name" {
  type        = string
  description = "Lowercase resource name prefix."
  default     = "aws-bank"
}

variable "environment" {
  type        = string
  description = "Deployment environment; development is the initial target."
  default     = "development"
}

variable "vpc_cidr" {
  type    = string
  default = "10.42.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.42.1.0/24"
}

variable "availability_zone" {
  type        = string
  description = "Optional single AZ. Empty selects the first available AZ in the region."
  default     = ""
}

variable "allowed_https_cidr_blocks" {
  type        = list(string)
  description = "Deprecated for the private phase; no inbound application access is enabled."
  default     = []
}

variable "instance_type" {
  type        = string
  description = "CPU-only instance candidate; validate t3.small versus t3.medium before deployment."
  default     = "t3.small"
}

variable "root_volume_size_gib" {
  type    = number
  default = 20
}

variable "data_volume_size_gib" {
  type        = number
  description = "Encrypted EBS volume for SQLite data and operational state."
  default     = 30
}

variable "image_uri" {
  type        = string
  description = "Required immutable ECR image URI including a digest or 40-64 character commit-SHA tag."
  default     = ""

  validation {
    condition     = trimspace(var.image_uri) != "" && (can(regex("@sha256:[0-9a-f]{64}$", var.image_uri)) || can(regex(":([0-9a-f]{40,64})$", var.image_uri)))
    error_message = "image_uri must be non-empty and end in an OCI SHA-256 digest or immutable 40-64 character commit-SHA tag."
  }
}

variable "ecr_repository_name" {
  type    = string
  default = "aws-bank"
}

variable "artifact_prefix" {
  type        = string
  description = "Prefix reserved for this environment's versioned model artifacts."
  default     = "models/development"
}

variable "bootstrap_password_parameter_name" {
  type        = string
  description = "Existing SSM SecureString parameter name; Terraform does not create or read its value."
  default     = "/banklab/development/bootstrap-password"
}

variable "session_secret_parameter_name" {
  type        = string
  description = "Existing SSM SecureString parameter name; Terraform does not create or read its value."
  default     = "/banklab/development/session-secret"
}

variable "ssm_kms_key_arn" {
  type        = string
  description = "Optional customer-managed KMS key ARN used by the SSM SecureString parameters."
  default     = ""
}

variable "budget_limit_usd" {
  type    = number
  default = 50
}

variable "budget_notification_emails" {
  type        = list(string)
  description = "Approved alert recipients; empty disables notification resources until configured."
  default     = []
}

variable "log_retention_days" {
  type    = number
  default = 30
}

variable "tags" {
  type    = map(string)
  default = {}
}
