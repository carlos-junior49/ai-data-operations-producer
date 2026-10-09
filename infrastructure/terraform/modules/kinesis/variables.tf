variable "stream_name" {
  description = "The name of the Kinesis stream."
  type        = string
}

variable "retention_period_hours" {
  description = "The number of hours to retain data in the Kinesis stream."
  type        = number
  default     = 24
  validation {
    condition     = var.retention_period_hours >= 24 && var.retention_period_hours <= 365 * 24
    error_message = "retention_period_hours must be between 24 and 365*24"
  }
}

variable "tags" {
  description = "A map of tags to apply to the Kinesis stream."
  type        = map(string)
  default     = {}
}