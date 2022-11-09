SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )

"$SCRIPTS_DIRECTORY"/etl_pipeline_deploy.sh
"$SCRIPTS_DIRECTORY"/airflow_up.sh
