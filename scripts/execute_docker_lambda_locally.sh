SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")


cd "$ROOT_DIRECTORY"/lambda_pivot_health_variables
docker build . -f Dockerfile --tag lambda-pivot-health-variables-image
docker run --publish 9000:8080 --name lambda-pivot-health-variables-container lambda-pivot-health-variables-image
