data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "app" {
  name               = "${var.project_name}-${var.environment}-ec2"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_instance_profile" "app" {
  name = "${var.project_name}-${var.environment}-ec2"
  role = aws_iam_role.app.name
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.app.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

data "aws_iam_policy_document" "app" {
  statement {
    sid       = "ArtifactBucketList"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.artifacts.arn]

    condition {
      test     = "StringLike"
      variable = "s3:prefix"
      values   = ["${var.artifact_prefix}/*"]
    }
  }

  statement {
    sid       = "ArtifactObjects"
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.artifacts.arn}/${var.artifact_prefix}/*"]
  }

  statement {
    sid       = "EcrRead"
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    sid       = "EcrRepositoryRead"
    effect    = "Allow"
    actions   = ["ecr:BatchCheckLayerAvailability", "ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"]
    resources = [aws_ecr_repository.app.arn]
  }

  statement {
    sid     = "ReadDeploymentParameters"
    effect  = "Allow"
    actions = ["ssm:GetParameter"]
    resources = [
      "arn:aws:ssm:${var.aws_region}:213473482400:parameter${var.bootstrap_password_parameter_name}",
      "arn:aws:ssm:${var.aws_region}:213473482400:parameter${var.session_secret_parameter_name}"
    ]
  }

  dynamic "statement" {
    for_each = var.ssm_kms_key_arn == "" ? [] : [var.ssm_kms_key_arn]

    content {
      sid       = "DecryptDeploymentParameters"
      effect    = "Allow"
      actions   = ["kms:Decrypt"]
      resources = [statement.value]
    }
  }

  statement {
    sid       = "WriteApplicationLogs"
    effect    = "Allow"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.app.arn}:*"]
  }

  statement {
    sid       = "StopOwnAwsBankInstance"
    effect    = "Allow"
    actions   = ["ec2:StopInstances"]
    resources = ["arn:aws:ec2:${var.aws_region}:213473482400:instance/*"]

    condition {
      test     = "StringLike"
      variable = "aws:userid"
      values   = ["*:$${ec2:InstanceID}"]
    }

    condition {
      test     = "ArnLike"
      variable = "ec2:SourceInstanceARN"
      values   = ["arn:aws:ec2:${var.aws_region}:213473482400:instance/*"]
    }
  }
}

resource "aws_iam_role_policy" "app" {
  name   = "${var.project_name}-${var.environment}-runtime"
  role   = aws_iam_role.app.id
  policy = data.aws_iam_policy_document.app.json
}
