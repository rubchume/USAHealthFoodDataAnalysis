from typing import Dict

import pandas as pd
import psycopg2


class PostgreSqlConnector(object):
    DEFAULT_DATABASE = "postgres"
    DEFAULT_USER = "postgres"
    DEFAULT_PASSWORD = "C407CmFS8JqhD8Hl5TB3"

    def __init__(self):
        self._connection = None
        self._cursor = None

    def connect(self, **kwargs):
        self._connection = self._get_connection(**kwargs)
        self._cursor = self._get_cursor()

    def disconnect(self):
        self._run_psycopg2_command(self._connection.close)
        self._run_psycopg2_command(self._cursor.close)

    def execute_sql(self, query, vars_list=None):
        self._run_psycopg2_command(self._cursor.execute, query, vars_list)
        return self._get_cursor_response()

    def list_databases(self):
        print(self.execute_sql("SELECT datname from pg_database"))

    def get_tables(self):
        return self.execute_sql(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )

    def get_table(self, table):
        columns = self._get_columns(table)
        column_names = [column.name for column in columns]

        entries = self._get_entries(table)

        return pd.DataFrame(entries, columns=column_names)

    def _get_columns(self, table):
        self.execute_sql(f"SELECT * FROM {table} LIMIT 0")
        return self._cursor.description

    def _get_entries(self, table):
        return self.execute_sql(f"SELECT * FROM {table}")

    def create_database(self, database_name):
        self.execute_sql(f"create database {database_name}")

    def create_table(self, table, columns: Dict[str, str]):
        columns_definition = ", ".join([
            f"{column_name} {column_type}"
            for column_name, column_type in columns.items()
        ])

        sql_statement = (
            "CREATE TABLE IF NOT EXISTS "
            f"{table} "
            f"({columns_definition});"

        )

        self.execute_sql(sql_statement)

    def drop_table(self, table):
        self.execute_sql(f"DROP TABLE {table}")

    def insert_into(self, table, values: dict):
        column_list = ", ".join(values.keys())
        values_list = list(values.values())
        value_template_list = ", ".join(["%s" for _ in range(len(values))])

        sql_statement = (
            "INSERT INTO "
            f"{table} "
            f"({column_list}) "
            f"VALUES ({value_template_list})"
        )

        self.execute_sql(sql_statement, values_list)

    @classmethod
    def _get_connection(cls, **kwargs):
        default_database_parameters = dict(
            user=cls.DEFAULT_USER,
            password=cls.DEFAULT_PASSWORD,
            database=cls.DEFAULT_DATABASE,
            host="localhost",
            port="5432"
        )

        database_parameters = default_database_parameters | kwargs

        connection = cls._run_psycopg2_command(
            psycopg2.connect,
            **database_parameters
        )

        connection.set_session(autocommit=True)

        return connection

    def _get_cursor(self):
        return self._run_psycopg2_command(self._connection.cursor)

    def _print_cursor_response(self):
        if self._is_response_empty():
            return

        rows = self._get_cursor_response()
        for row in rows:
            print(row)

    def _get_cursor_response(self):
        if self._is_response_empty():
            return

        return [
            row[0] if len(row) == 1
            else row
            for row in self._cursor
        ]

    def _is_response_empty(self):
        return self._cursor.description is None

    @staticmethod
    def _run_psycopg2_command(function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except psycopg2.Error as e:
            print(e)