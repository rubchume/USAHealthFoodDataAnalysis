provider "aws" {
	region = var.aws_region
	profile = var.aws_profile
}

#module "storage" {
#  source = "git::https://github.com/rubchume/TerraformAWSexamples//aws_redshift_example?ref=353c077404bbc5612cdc7d8b044c74c7a2a945ab"
#
#  aws_region  = var.aws_profile
#  aws_profile = var.aws_profile
#
#  dwh_iam_role_name = var.dwh_iam_role_name
#
#  vpc_cidr               = "10.0.0.0/16"
#  redshift_subnet_cidr_1 = "10.0.1.0/24"
#  redshift_subnet_cidr_2 = "10.0.2.0/24"
#
#  subnet_availability_zone = "${var.aws_region}a"
#
#  rs_cluster_identifier      = "dwh-cluster"
#  rs_database_name           = var.database_name
#  rs_master_username         = var.login
#  rs_master_pass             = var.password
#  rs_nodetype                = "dc2.large"
#  rs_cluster_type            = "single-node"
#  rs_cluster_number_of_nodes = 1
#}


#resource "aws_s3_bucket" "s3" {
#  bucket = var.s3_bucket
#
#  tags = {
#    Name        = "Udacity Nanodegree Capstone Project Bucket"
#    Environment = "Dev"
#  }
#}


module "lambda_function" {
  source = "./aws_lambda"

  function_name = "lambda_pivot_variables"
  lambda_image_ecr_uri = var.lambda_image_uri
}


module "api_gateway" {
  source = "./aws_api_gateway_for_lambda"

  aws_lambda_function = module.lambda_function.aws_lambda_resource
}
