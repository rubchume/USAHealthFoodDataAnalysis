source .env

SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )
ROOT_DIRECTORY=$(dirname "$SCRIPTS_DIRECTORY")

cd "$ROOT_DIRECTORY"/terraform/etl_pipeline_infrastructure || exit
REDSHIFT_HOST=$(terraform output --raw redshift_host)
REDSHIFT_PORT=$(terraform output --raw redshift_port)

cd "$ROOT_DIRECTORY"/airflow || exit
docker-compose -f docker-compose.yaml up --detach

docker exec airflow_scheduler airflow variables set s3_bucket "$s3_bucket"
docker exec airflow_scheduler airflow variables set county_state_data_csv_name "$county_state_data_csv_name"
docker exec airflow_scheduler airflow variables set county_supplemental_data_csv_name "$county_supplemental_data_csv_name"
docker exec airflow_scheduler airflow variables set state_supplemental_data_csv_name "$state_supplemental_data_csv_name"

IAM_ROLE_ARN=arn:aws:iam::$account_id:role/$redshiftIAMRole
docker exec airflow_scheduler airflow variables set iam_role_arn $IAM_ROLE_ARN

docker exec airflow_scheduler airflow connections delete postgres_default
docker exec airflow_scheduler airflow connections add 'postgres_default' \
    --conn-json '{
            "conn_type": "postgres",
            "login": "'$login'",
            "password": "'$password'",
            "host": "'$REDSHIFT_HOST'",
            "port": '$REDSHIFT_PORT',
            "schema": "'$database_name'"
        }'

docker exec airflow_scheduler airflow connections delete redshift_default
docker exec airflow_scheduler airflow connections add 'redshift_default' \
    --conn-json '{
            "conn_type": "redshift",
            "login": "'$login'",
            "password": "'$password'",
            "host": "'$REDSHIFT_HOST'",
            "port": '$REDSHIFT_PORT',
            "schema": "'$database_name'",
            "extra": {
                "region": "'$aws_region'"
            }
        }'
