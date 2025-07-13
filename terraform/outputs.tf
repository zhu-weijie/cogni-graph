output "ecr_repository_url" {
  description = "The URL of the ECR repository for the API."
  value       = aws_ecr_repository.api.repository_url
}

output "oidc_role_arn" {
  description = "The ARN of the IAM role for GitHub Actions CD."
  value       = aws_iam_role.github_actions_cd.arn
}

output "rds_master_password_secret_arn" {
  description = "The ARN of the automatically generated RDS master password secret."
  value       = aws_db_instance.main.master_user_secret[0].secret_arn
}