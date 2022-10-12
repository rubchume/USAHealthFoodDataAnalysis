provider "aws" {
	region = var.aws_region
	profile = var.aws_profile
}

module "storage" {
  source = "git::https://github.com/rubchume/TerraformAWSexamples//aws_redshift_example?ref=353c077404bbc5612cdc7d8b044c74c7a2a945ab"

  aws_region  = "eu-west-3"
  aws_profile = "udacity_student"

  dwh_iam_role_name = "dwhRole"

  vpc_cidr               = "10.0.0.0/16"
  redshift_subnet_cidr_1 = "10.0.1.0/24"
  redshift_subnet_cidr_2 = "10.0.2.0/24"

  subnet_availability_zone = "eu-west-3a"

  rs_cluster_identifier      = "dwh-cluster"
  rs_database_name           = var.database_name
  rs_master_username         = var.login
  rs_master_pass             = var.password
  rs_nodetype                = "dc2.large"
  rs_cluster_type            = "single-node"
  rs_cluster_number_of_nodes = 1
}

resource "aws_s3_bucket" "s3" {
  bucket = "udacity-nanodegree-capstone-project"

  tags = {
    Name        = "Udacity Nanodegree Capstone Project Bucket"
    Environment = "Dev"
  }
}
