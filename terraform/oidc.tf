resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]

  thumbprint_list = ["1b511abead59c6ce207077c0bf0e0043b1382612"]
}

data "aws_iam_policy_document" "github_actions_cd_policy" {
  statement {
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage",
      "eks:DescribeCluster"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "github_actions_cd" {
  name   = "cogni-graph-github-actions-cd-policy"
  policy = data.aws_iam_policy_document.github_actions_cd_policy.json
}

resource "aws_iam_role" "github_actions_cd" {
  name = "cogni-graph-github-actions-cd-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        },
        Action    = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:zhu-weijie/cogni-graph:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "github_actions_cd" {
  role       = aws_iam_role.github_actions_cd.name
  policy_arn = aws_iam_policy.github_actions_cd.arn
}