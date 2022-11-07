source .env

SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd "$ROOT_DIRECTORY"/terraform/lambda_ecr_image || exit
REPOSITORY_URL=$(terraform output -json ecr_scraper_repository_url | jq --raw-output ".repository_url")

cd "$ROOT_DIRECTORY"/terraform/etl_pipeline_infrastructure || exit
terraform init
terraform get -update
terraform apply -lock=false \
  -var="database_name=$database_name" \
  -var="login=$login" \
  -var="password=$password" \
  -var="aws_region=$aws_region" \
  -var="aws_profile=$aws_profile" \
  -var="s3_bucket=$s3_bucket" \
  -var="dwh_iam_role_name=$redshiftIAMRole" \
  -var="lambda_image_uri=$REPOSITORY_URL" \
  -auto-approve

