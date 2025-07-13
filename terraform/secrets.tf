resource "aws_secretsmanager_secret" "db_password" {
  name        = "cogni-graph-db-password"
  description = "Password for the CogniGraph RDS database managed by RDS"
}

resource "aws_secretsmanager_secret" "neo4j_password" {
  name        = "cogni-graph-neo4j-password"
  description = "Password for the Neo4j database"
}

resource "aws_secretsmanager_secret_version" "neo4j_password_version" {
  secret_id = aws_secretsmanager_secret.neo4j_password.id

  secret_string = jsonencode({
    password = random_password.neo4j.result
  })
}

resource "random_password" "neo4j" {
  length           = 16
  special          = true
  override_special = "!#%&"
}