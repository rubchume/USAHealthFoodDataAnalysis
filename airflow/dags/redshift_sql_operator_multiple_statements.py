from pathlib import Path

from airflow.models.baseoperator import BaseOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
import sqlparse


class RedshiftSQLOperatorMultipleStatements(BaseOperator):
    def __init__(self, sql_file: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sql_file = sql_file

    def execute(self, context):
        sql_statements = self.get_sql_statements(self.sql_file)

        for sql_statement in sql_statements:
            redshift_sql_operator = RedshiftSQLOperator(
                task_id=self.task_id,
                sql=sql_statement
            )
            redshift_sql_operator.execute(dict())

    @staticmethod
    def get_sql_statements(sql_file):
        # print(list(Path(".").glob('**/*.py')))
        with Path(sql_file).open("r") as file:
            sql_string = file.read()
            return sqlparse.split(sql_string)
