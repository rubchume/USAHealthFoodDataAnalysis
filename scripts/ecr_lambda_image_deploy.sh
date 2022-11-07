source .env

SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd $ROOT_DIRECTORY/terraform/lambda_ecr_image || exit
terraform init
terraform get -update
terraform apply -lock=false \
  -var="aws_region=$aws_region" \
  -var="aws_profile=$aws_profile" \
  -auto-approve

