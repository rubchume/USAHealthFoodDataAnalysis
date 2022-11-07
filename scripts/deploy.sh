SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )

"$SCRIPTS_DIRECTORY"/ecr_lambda_image_deploy.sh
"$SCRIPTS_DIRECTORY"/push_lambda_docker_image.sh
"$SCRIPTS_DIRECTORY"/etl_pipeline_deploy.sh
"$SCRIPTS_DIRECTORY"/airflow_up.sh
