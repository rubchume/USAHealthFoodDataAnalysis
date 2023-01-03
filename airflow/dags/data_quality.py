from dataclasses import dataclass
import logging
from typing import Any, List, Callable

from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

task_logger = logging.getLogger('airflow.task')


@dataclass
class DataQualityCheck:
    sql_statement: str
    expected_result: Any
    match_function: Callable = None


class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    def __init__(
            self,
            checks: List[DataQualityCheck],
            postgres_conn_id="postgres_default",
            *args,
            **kwargs
    ):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        hook = PostgresHook(postgres_conn_id=postgres_conn_id)
        conn = hook.get_conn()
        self.cursor = conn.cursor()
        self.checks = checks

    def execute(self, context):
        for check in self.checks:
            self.execute_check(check)
            task_logger.info("Check passed")

    def execute_check(self, check: DataQualityCheck):
        self.cursor.execute(check.sql_statement)
        response = self._get_cursor_response()
        match_function = check.match_function or self._equality_match_function
        if not match_function(response[0], check.expected_result):
            raise ValueError(
                f"Data quality check failed. Response: {response[0]}. Expected result: {check.expected_result}")

    @staticmethod
    def _equality_match_function(response, expected):
        return response == expected

    def _get_cursor_response(self):
        if self._is_response_empty():
            return

        return [
            row[0] if len(row) == 1
            else row
            for row in self.cursor
        ]

    def _is_response_empty(self):
        return self.cursor.description is None
