SCRIPTS_DIRECTORY=$( cd "$(dirname "$0")" ; pwd -P )

"$SCRIPTS_DIRECTORY"/terraform_destroy.sh
"$SCRIPTS_DIRECTORY"/airflow_down.sh
