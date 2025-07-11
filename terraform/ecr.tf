resource "aws_ecr_repository" "api" {
  name = "cogni-graph-api"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "IMMUTABLE"

  tags = {
    Project = "cogni-graph"
  }
}