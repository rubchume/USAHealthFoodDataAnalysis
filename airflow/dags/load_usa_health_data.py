from datetime import datetime

from airflow.decorators import dag, task
from airflow.models.variable import Variable
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.http.operators.http import SimpleHttpOperator


@dag(
    schedule_interval="@once",
    catchup=False,
    start_date=datetime.now()
)
def load_usa_health_data():
    execute_lambda = SimpleHttpOperator(
        task_id="pivot_variables",
        http_conn_id="lambda_connection",
        endpoint='pivot_variables',
        method="GET",
        data={
            "bucket": Variable.get("s3_bucket"),
            "input_file": Variable.get("state_and_county_data_csv_name"),
            "output_file": Variable.get("state_and_county_data_pivoted_csv_name")
        },
        response_check=lambda response: response.status_code == 200
    )
    # create_tables = RedshiftSQLOperator(
    #     task_id="create_tables",
    #     sql="sql/create_tables.sql",
    # )
    #
    # load_staging_data = RedshiftSQLOperator(
    #     task_id="load_staging_data",
    #     sql="sql/load_data.sql",
    #     params=dict(
    #         s3_bucket=Variable.get("s3_bucket"),
    #         csv_name=Variable.get("state_and_county_data_csv_name"),
    #         iam_role=Variable.get("iam_role_arn")
    #     )
    # )
    #
    # create_tables >> load_staging_data


dag = load_usa_health_data()
