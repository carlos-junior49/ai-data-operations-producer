module "kinesis" {
  source           = "../../modules/kinesis"
  stream_name      = var.kinesis_stream_name
  retention_period_hours = var.kinesis_retention_period_hours

  tags = {
    Enviroment  = "dev"
    Application = "e-comerce"
  }
}