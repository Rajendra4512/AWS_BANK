resource "aws_security_group" "app" {
  name        = "${var.project_name}-${var.environment}-app"
  description = "Private AWS_BANK instance; application access is through SSM port forwarding"
  vpc_id      = aws_vpc.main.id

  egress {
    description = "Outbound package, ECR, S3, SSM and CloudWatch access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
