resource "aws_elasticache_subnet_group" "main" {
  name       = "cogni-graph-redis-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Project = "cogni-graph"
  }
}

resource "aws_security_group" "redis" {
  name        = "cogni-graph-redis-sg"
  description = "Allow traffic to the ElastiCache Redis cluster"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
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

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "cogni-graph-redis"
  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]

  tags = {
    Project = "cogni-graph"
  }
}