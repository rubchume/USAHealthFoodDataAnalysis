from datetime import datetime
import json

from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.models.variable import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    schedule_interval="@once",
    catchup=False,
    start_date=datetime.now()
)
def load_usa_health_data():
    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="postgres_default",
        sql="sql/create_tables.sql",
    )

    # load_staging_data = PostgresOperator(
    #     task_id="load_staging_data",
    #     postgres_conn_id="postgres_default",
    #     sql="sql/load_data.sql",
    #     parameters=dict(
    #         s3_bucket=Variable.get("s3_bucket"),
    #         csv_name=Variable.get("state_and_county_data_csv_name"),
    #         aws_region=json.loads(BaseHook.get_connection("postgres_default").get_extra())["region"],
    #     )
    # )


dag = load_usa_health_data()
