source .env

SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd "$ROOT_DIRECTORY"/lambda_pivot_health_variables
docker build . -f Dockerfile --tag lambda-pivot-health-variables-image

# Load variables
cd "$ROOT_DIRECTORY"/terraform/lambda_ecr_image
ECR_REGISTRY_URL=$(terraform output -json ecr_scraper_repository_url | jq --raw-output ".registry_url")
REPOSITORY_URL=$(terraform output -json ecr_scraper_repository_url | jq --raw-output ".repository_url")

# Retrieve authentication token
TOKEN=$(aws ecr get-login-password --region $aws_region --profile $aws_profile)

## Authenticate docker
echo $ECR_REGISTRY_URL
docker login --username AWS --password $TOKEN $ECR_REGISTRY_URL

# Tag image
docker tag lambda-pivot-health-variables-image:latest $REPOSITORY_URL:latest

# Push image
docker push $REPOSITORY_URL:latest
