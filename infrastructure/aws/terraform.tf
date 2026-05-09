provider "aws" {
  region = "ap-south-1" # Hosted in India for DPDP Data Residency Compliance
}

# S3 Bucket for Raw Data Lake
resource "aws_s3_bucket" "bkg_data_lake" {
  bucket = "healthcare-bkg-data-lake"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bkg_encryption" {
  bucket = aws_s3_bucket.bkg_data_lake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# PostgreSQL Database (RDS) with PostGIS
resource "aws_db_instance" "bkg_postgres" {
  allocated_storage    = 100
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.medium"
  db_name              = "healthcare_bkg"
  username             = "admin"
  password             = "password123" # TODO: Move to AWS Secrets Manager
  skip_final_snapshot  = true
}

# Amazon Neptune (Graph DB)
resource "aws_neptune_cluster" "bkg_neptune" {
  cluster_identifier                  = "healthcare-bkg-neptune"
  engine                              = "neptune"
  skip_final_snapshot                 = true
  iam_database_authentication_enabled = true
}

resource "aws_neptune_cluster_instance" "bkg_neptune_instances" {
  count              = 1
  cluster_identifier = aws_neptune_cluster.bkg_neptune.id
  engine             = "neptune"
  instance_class     = "db.r5.large"
}

# ElastiCache (Redis)
resource "aws_elasticache_cluster" "bkg_redis" {
  cluster_id           = "healthcare-bkg-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}
