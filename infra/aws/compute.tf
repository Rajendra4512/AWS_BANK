resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile   = aws_iam_instance_profile.app.name
  # No inbound SG rules are defined. A public IP is retained only because this
  # no-NAT development subnet needs outbound bootstrap/SSM/ECR/S3 connectivity.
  associate_public_ip_address = true
  user_data_replace_on_change = false

  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    aws_region                   = var.aws_region
    image_uri                    = var.image_uri
    bucket_name                  = aws_s3_bucket.artifacts.bucket
    artifact_prefix              = var.artifact_prefix
    bootstrap_password_parameter = var.bootstrap_password_parameter_name
    session_secret_parameter     = var.session_secret_parameter_name
    log_group_name               = aws_cloudwatch_log_group.app.name
    data_volume_id               = aws_ebs_volume.data.id
  })

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    encrypted   = true
    volume_type = "gp3"
    volume_size = var.root_volume_size_gib
  }

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}

resource "aws_volume_attachment" "data" {
  device_name = "/dev/sdf"
  volume_id   = aws_ebs_volume.data.id
  instance_id = aws_instance.app.id
}
