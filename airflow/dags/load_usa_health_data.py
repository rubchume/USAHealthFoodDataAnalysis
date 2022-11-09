from datetime import datetime

from airflow.decorators import dag, task
from airflow.models.variable import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.http.operators.http import SimpleHttpOperator


@dag(
    schedule_interval="@once",
    catchup=False,
    start_date=datetime.now()
)
def load_usa_health_data():
    create_tables = RedshiftSQLOperator(
        task_id="create_tables",
        sql="sql/create_tables.sql",
    )

    load_staging_data = RedshiftSQLOperator(
        task_id="load_staging_data",
        sql="sql/load_data.sql",
        params=dict(
            s3_bucket=Variable.get("s3_bucket"),
            csv_name=Variable.get("state_and_county_data_csv_name"),
            iam_role=Variable.get("iam_role_arn")
        )
    )

    @task(task_id="get_variable_codes")
    def get_variable_codes(**context):
        hook = PostgresHook(postgres_conn_id="postgres_default")
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT Variable_Code FROM county_state_health_data_staging")
        sources = cursor.fetchall()
        variable_codes = [
            f"'{source[0]}'"
            for source in sources
        ]
        return ", ".join(variable_codes)

    get_variable_codes_task = get_variable_codes()

    pivot_table = RedshiftSQLOperator(
        task_id="pivot_table",
        sql="sql/pivot_table.sql",
    )

    create_tables >> load_staging_data >> get_variable_codes_task >> pivot_table


dag = load_usa_health_data()
