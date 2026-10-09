output "kinesis_stream_name" {
  description = "The name of the Kinesis stream"
  value       = module.kinesis.stream_name
}

output "kinesis_stream_arn" {
  description = "The ARN of the Kinesis stream"
  value       = module.kinesis.stream_arn
}
