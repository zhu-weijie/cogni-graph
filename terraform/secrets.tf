resource "aws_secretsmanager_secret" "db_password" {
  name = "cogni-graph-db-password"
  description = "Password for the CogniGraph RDS database"
}