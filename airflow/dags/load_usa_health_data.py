from datetime import datetime

from airflow.decorators import dag, task
from airflow.models.variable import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator

from redshift_sql_operator_multiple_statements import RedshiftSQLOperatorMultipleStatements


@dag(
    schedule_interval="@once",
    catchup=False,
    start_date=datetime.now()
)
def load_usa_health_data():
    create_county_state_data_table = RedshiftSQLOperator(
        task_id="create_county_state_data_table",
        sql="sql/create_county_state_data_table.sql",
    )

    create_supplemental_county_data_table = RedshiftSQLOperator(
        task_id="create_supplemental_county_data_table",
        sql="sql/create_supplemental_county_data_table.sql",
    )

    create_supplemental_state_data_table = RedshiftSQLOperator(
        task_id="create_supplemental_state_data_table",
        sql="sql/create_supplemental_state_data_table.sql",
    )

    load_county_state_data = RedshiftSQLOperator(
        task_id="load_county_state_data",
        sql="sql/load_county_state_data.sql",
        params=dict(
            s3_bucket=Variable.get("s3_bucket"),
            county_state_data_csv_name=Variable.get("county_state_data_csv_name"),
            iam_role=Variable.get("iam_role_arn")
        )
    )

    load_supplemental_county_data = RedshiftSQLOperator(
        task_id="load_supplemental_county_data",
        sql="sql/load_supplemental_county_data.sql",
        params=dict(
            s3_bucket=Variable.get("s3_bucket"),
            county_supplemental_data_csv_name=Variable.get("county_supplemental_data_csv_name"),
            iam_role=Variable.get("iam_role_arn")
        )
    )

    load_supplemental_state_data = RedshiftSQLOperator(
        task_id="load_supplemental_state_data",
        sql="sql/load_supplemental_state_data.sql",
        params=dict(
            s3_bucket=Variable.get("s3_bucket"),
            state_supplemental_data_csv_name=Variable.get("state_supplemental_data_csv_name"),
            iam_role=Variable.get("iam_role_arn")
        )
    )

    unite_county_data = RedshiftSQLOperator(
        task_id="unite_county_data",
        sql="sql/unite_county_data.sql",
    )

    @task(task_id="get_variable_codes")
    def get_count_state_variable_codes(**context):
        hook = PostgresHook(postgres_conn_id="postgres_default")
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT Variable_Code FROM AllCountyDataStaging")
        sources = cursor.fetchall()
        variable_codes = [
            f"'{source[0]}'"
            for source in sources
        ]
        return ", ".join(variable_codes)

    get_count_state_variable_codes_task = get_count_state_variable_codes()

    pivot_county_state_data_table = RedshiftSQLOperator(
        task_id="pivot_county_state_data_table",
        sql="sql/pivot_county_state_data_table.sql",
    )

    divide_into_county_health_data_and_county_data_tables = RedshiftSQLOperatorMultipleStatements(
        sql_file="dags/sql/divide_into_county_health_data_and_county_data_tables.sql",
        task_id="divide_into_county_health_data_and_county_data_tables",
    )

    @task(task_id="get_variable_codes")
    def get_state_variable_codes(**context):
        hook = PostgresHook(postgres_conn_id="postgres_default")
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT Variable_Code FROM SupplementalDataStateStaging")
        sources = cursor.fetchall()
        variable_codes = [
            f"'{source[0]}'"
            for source in sources
        ]
        return ", ".join(variable_codes)

    get_state_variable_codes_task = get_state_variable_codes()

    pivot_state_table = RedshiftSQLOperator(
        task_id="pivot_state_data_table",
        sql="sql/pivot_state_data_table.sql",
    )

    divide_into_health_data_and_state_data_tables = RedshiftSQLOperatorMultipleStatements(
        sql_file="dags/sql/divide_into_health_data_and_state_data_tables.sql",
        task_id="divide_into_health_data_and_state_data_tables",
    )

    create_county_state_data_table >> load_county_state_data >> unite_county_data
    create_supplemental_county_data_table >> load_supplemental_county_data >> unite_county_data
    unite_county_data >> get_count_state_variable_codes_task >> pivot_county_state_data_table \
    >> divide_into_county_health_data_and_county_data_tables
    (
            create_supplemental_state_data_table
            >> load_supplemental_state_data
            >> get_state_variable_codes_task
            >> pivot_state_table
            >> divide_into_health_data_and_state_data_tables
    ) >> divide_into_county_health_data_and_county_data_tables


dag = load_usa_health_data()
