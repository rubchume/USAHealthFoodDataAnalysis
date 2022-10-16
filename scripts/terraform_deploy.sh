source .env

SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd $ROOT_DIRECTORY/terraform || exit
terraform init
terraform get -update
terraform apply -lock=false \
  -var="database_name=$database_name" \
  -var="login=$login" \
  -var="password=$password" \
  -var="aws_region=$aws_region" \
  -var="s3_bucket=$s3_bucket" \
  -var="dwh_iam_role_name=$redshiftIAMRole" \
  -auto-approve

