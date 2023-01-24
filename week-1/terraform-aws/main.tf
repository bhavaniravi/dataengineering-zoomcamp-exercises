terraform {
  required_version = ">= 1.0"
  backend "local" {} # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = "produser"
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "aws_s3_bucket" "data-lake-bucket" {
  bucket = local.data_lake_bucket
}


resource "aws_redshift_cluster" "example" {
  cluster_identifier  = "tf-redshift-cluster"
  database_name       = var.BQ_DATASET
  master_username     = "exampleuser"
  master_password     = "examplePass1"
  node_type           = "dc2.large"
  cluster_type        = "single-node"
  skip_final_snapshot = true
}
