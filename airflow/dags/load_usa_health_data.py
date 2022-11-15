from datetime import datetime

from airflow.decorators import dag, task
from airflow.decorators.task_group import task_group
from airflow.models.variable import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

from redshift_sql_operator_multiple_statements import RedshiftSQLOperatorMultipleStatements


@dag(
    schedule_interval="@once",
    catchup=False,
    start_date=datetime.now()
)
def upload_csv_files_to_s3():
    upload_vaccinations_csv = LocalFilesystemToS3Operator(
        task_id="upload_vaccinations_csv",
        filename="./data/COVID-19_Vaccinations_in_the_United_States_County.csv",
        dest_key=Variable.get("covid_vaccinations_csv_name"),
        dest_bucket=Variable.get("s3_bucket"),
        aws_conn_id="aws_s3_connection",
        replace=False,
    )

    upload_covid_cases_csv = LocalFilesystemToS3Operator(
        task_id="upload_covid_cases_csv",
        filename="./data/CovidCases.csv",
        dest_key=Variable.get("covid_cases_data_csv_name"),
        dest_bucket=Variable.get("s3_bucket"),
        aws_conn_id="aws_s3_connection",
        replace=False,
    )

    @task_group(group_id="upload_nutrition_csvs")
    def upload_nutrition_csvs_group():
        upload_state_and_county_csv = LocalFilesystemToS3Operator(
            task_id="upload_state_and_county_csv",
            filename="./data/StateAndCountyData.csv",
            dest_key=Variable.get("county_state_data_csv_name"),
            dest_bucket=Variable.get("s3_bucket"),
            aws_conn_id="aws_s3_connection",
            replace=False,
        )

        upload_supplemental_data_county_csv = LocalFilesystemToS3Operator(
            task_id="upload_supplemental_data_county_csv",
            filename="./data/SupplementalDataCounty.csv",
            dest_key=Variable.get("county_supplemental_data_csv_name"),
            dest_bucket=Variable.get("s3_bucket"),
            aws_conn_id="aws_s3_connection",
            replace=False,
        )

        upload_supplemental_data_state_csv = LocalFilesystemToS3Operator(
            task_id="upload_supplemental_data_state_csv",
            filename="./data/SupplementalDataState.csv",
            dest_key=Variable.get("state_supplemental_data_csv_name"),
            dest_bucket=Variable.get("s3_bucket"),
            aws_conn_id="aws_s3_connection",
            replace=False,
        )

    upload_nutrition_csvs_group()


upload_csvs_dag = upload_csv_files_to_s3()


@dag(
    schedule_interval="@once",
    catchup=False,
    start_date=datetime.now()
)
def load_usa_health_data():
    @task_group(group_id="nutrition_data")
    def nutrition_data_group():
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

    @task_group(group_id="covid_cases")
    def covid_cases_group():
        create_covid_cases_table = RedshiftSQLOperator(
            task_id="create_covid_cases_table",
            sql="sql/create_covid_cases_table.sql",
        )

        load_covid_cases = RedshiftSQLOperator(
            task_id="load_covid_cases_data",
            sql="sql/load_covid_cases_data.sql",
            params=dict(
                s3_bucket=Variable.get("s3_bucket"),
                covid_cases_data_csv_name=Variable.get("covid_cases_data_csv_name"),
                iam_role=Variable.get("iam_role_arn")
            )
        )

        create_covid_cases_table >> load_covid_cases

    @task_group(group_id="covid_vaccination")
    def covid_vaccination_group():
        create_covid_vaccination_table = RedshiftSQLOperator(
            task_id="create_covid_vaccination_table",
            sql="sql/create_covid_vaccination_table.sql",
        )

        load_covid_vaccination = RedshiftSQLOperator(
            task_id="load_covid_vaccination",
            sql="sql/load_covid_vaccinations.sql",
            params=dict(
                s3_bucket=Variable.get("s3_bucket"),
                covid_vaccinations_csv_name=Variable.get("covid_vaccinations_csv_name"),
                iam_role=Variable.get("iam_role_arn")
            )
        )

        create_covid_vaccination_table >> load_covid_vaccination

    nutrition_data_group_task = nutrition_data_group()
    covid_cases_group_task = covid_cases_group()
    covid_vaccination_group_task = covid_vaccination_group()


dag = load_usa_health_data()
