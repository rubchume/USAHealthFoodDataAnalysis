from datetime import datetime

from airflow.decorators import dag, task
from airflow.models.variable import Variable
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator


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

    create_tables >> load_staging_data


dag = load_usa_health_data()
