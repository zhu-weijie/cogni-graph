data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [module.vpc.vpc_id]
  }
  tags = {
    "kubernetes.io/cluster/cogni-graph-eks" = "shared"
  }
}

resource "aws_eks_cluster" "main" {
  name     = "cogni-graph-eks"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.30"

  vpc_config {
    subnet_ids = module.vpc.private_subnets
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
  ]

  tags = {
    Project = "cogni-graph"
  }
}