provider "aws" {
	region = var.aws_region
	profile = var.aws_profile
}


module "ecr_lambda_repositories" {
  source="git::https://github.com/rubchume/TerraformAWSexamples.git//modules/aws_ecr_repositories"

  repository_names = ["lambda_image"]
}
