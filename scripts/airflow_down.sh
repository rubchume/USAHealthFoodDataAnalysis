SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd $ROOT_DIRECTORY/airflow
docker-compose -f docker-compose.yaml down
