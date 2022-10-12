source .env

SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd "$ROOT_DIRECTORY"/terraform
REDSHIFT_HOST=$(terraform output --raw redshift_host)
REDSHIFT_PORT=$(terraform output --raw redshift_port)

cd $ROOT_DIRECTORY/airflow
docker-compose -f docker-compose.yaml up --detach

docker exec airflow_scheduler airflow connections delete postgres_default
docker exec airflow_scheduler airflow connections add 'postgres_default' \
    --conn-type postgres \
    --conn-login $login \
    --conn-password $password \
    --conn-host $REDSHIFT_HOST \
    --conn-port $REDSHIFT_PORT \
    --conn-schema $database_name
