resource "helm_release" "neo4j" {
  name       = "neo4j"
  repository = "https://neo4j.github.io/helm-charts"
  chart      = "neo4j"
  namespace  = "default"
  version    = "5.17.0"

  set {
    name  = "neo4j.name"
    value = "cogni-graph-neo4j"
  }
  set {
    name  = "acceptLicenseAgreement"
    value = "yes"
  }
  set {
    name  = "plugins.apoc"
    value = "true"
  }
  set {
    name  = "volumes.data.mode"
    value = "persistent-volume"
  }

  set_sensitive {
    name  = "neo4j.password"
    value = random_password.neo4j.result
  }

  depends_on = [
    aws_secretsmanager_secret_version.neo4j_password_version
  ]
}