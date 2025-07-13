resource "aws_iam_role" "eks_cluster" {
  name = "cogni-graph-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = {
          Service = "eks.amazonaws.com"
        },
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = "cogni-graph"
  }
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_iam_role" "eks_nodes" {
  name = "cogni-graph-eks-node-group-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action    = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = "cogni-graph"
  }
}

resource "aws_iam_role_policy_attachment" "eks_nodes_worker_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_nodes_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_nodes_ecr_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_policy" "secrets_manager_read" {
  name        = "cogni-graph-secrets-read-policy"
  description = "Allows reading specific secrets from Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Effect = "Allow",
        Resource = [
          "arn:aws:secretsmanager:${var.aws_region}:${var.aws_account_id}:secret:cogni-graph/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_nodes_secrets_policy" {
  policy_arn = aws_iam_policy.secrets_manager_read.arn
  role       = aws_iam_role.eks_nodes.name
}

data "aws_iam_policy_document" "secrets_store_csi_driver_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type = "Federated"
      identifiers = [
        aws_iam_openid_connect_provider.main.arn
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.main.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:secrets-store-csi-driver"]
    }
  }
}

resource "aws_iam_role" "secrets_store_csi_driver" {
  name               = "cogni-graph-secrets-store-csi-role"
  assume_role_policy = data.aws_iam_policy_document.secrets_store_csi_driver_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "secrets_store_csi_driver_policy" {
  policy_arn = aws_iam_policy.secrets_manager_read.arn
  role       = aws_iam_role.secrets_store_csi_driver.name
}