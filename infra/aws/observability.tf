resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/${var.project_name}/${var.environment}"
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_log_metric_filter" "health_errors" {
  name           = "${var.project_name}-${var.environment}-error-count"
  pattern        = "ERROR"
  log_group_name = aws_cloudwatch_log_group.app.name

  metric_transformation {
    name      = "ApplicationErrors"
    namespace = "AWS_BANK/${var.environment}"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "health_errors" {
  alarm_name          = "${var.project_name}-${var.environment}-application-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApplicationErrors"
  namespace           = "AWS_BANK/${var.environment}"
  period              = 300
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Application log errors exceeded the offline-prepared threshold."
  treat_missing_data  = "notBreaching"
}
