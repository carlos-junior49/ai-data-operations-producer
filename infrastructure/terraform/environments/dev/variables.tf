variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
  default     = "us-east-2"
}

variable "kinesis_stream_name" {
  description = "Name of the development enviroment."
  type        = string
  default     = "ai-data-operations-events"
}

variable "kinesis_retention_period_hours" {
  description = "The retention period for the Kinesis stream in hours."
  type        = number
  default     = 24
}
