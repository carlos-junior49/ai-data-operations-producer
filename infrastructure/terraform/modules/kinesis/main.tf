resource "aws_kinesis_stream" "this" {
  name             = var.stream_name
  retention_period = var.retention_period_hours

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis"

  tags = merge(
    var.tags,
    {
      Name      = var.stream_name
      Project   = "AI-Data-Operations"
      ManagedBy = "Terraform"
    }
  )
}