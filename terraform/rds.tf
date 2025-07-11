resource "aws_db_subnet_group" "main" {
  name       = "cogni-graph-rds-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Project = "cogni-graph"
  }
}

resource "aws_security_group" "rds" {
  name        = "cogni-graph-rds-sg"
  description = "Allow traffic to the RDS instance"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_eks_cluster.main.vpc_config[0].cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project = "cogni-graph"
  }
}

resource "aws_db_instance" "main" {
  identifier           = "cogni-graph-db"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "16"
  instance_class       = "db.t3.micro"
  db_name              = "cogni_graph_db"
  username             = "cogni_user"
  password             = "password" 
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot  = true

  tags = {
    Project = "cogni-graph"
  }
}