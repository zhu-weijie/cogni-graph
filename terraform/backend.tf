terraform {
  backend "s3" {
    bucket = "cogni-graph-terraform-state-bucket-unique-name"
    key    = "global/terraform.tfstate"
    region = "ap-southeast-1"

    dynamodb_table = "cogni-graph-terraform-locks"
  }
}