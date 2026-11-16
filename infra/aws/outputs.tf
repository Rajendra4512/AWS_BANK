output "region" {
  value = var.aws_region
}

output "instance_id" {
  value = aws_instance.app.id
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "artifact_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "artifact_prefix" {
  value = var.artifact_prefix
}

output "cloudwatch_log_group" {
  value = aws_cloudwatch_log_group.app.name
}
