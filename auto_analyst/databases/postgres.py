from auto_analyst.databases.base import BaseDatabase
import psycopg2
from psycopg2 import sql
from typing import List
import pandas as pd
from contextlib import closing


class PostgresDatabase(BaseDatabase):
    """Production level implementation of BaseDatabase for Postgres"""

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        """Initialize PostgresDatabase with connection details"""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def _connect(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def run_query(self, query: str) -> pd.DataFrame:
        """Run query using Postgres"""
        with closing(self._connect()) as conn:
            return pd.read_sql_query(query, conn)

    def get_tables(self) -> List[str]:
        """List tables in Postgres"""
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
        with closing(self._connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)
                return [table[0] for table in cursor.fetchall()]

    def get_schema(self, table_name: str) -> pd.DataFrame:
        """Get schema for the given table in Postgres"""
        query = sql.SQL(
            """
            SELECT column_name, data_type 
            FROM information_schema.columns
            WHERE table_name = {}
        """
        ).format(sql.Identifier(table_name))

        with closing(self._connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query)
                return pd.DataFrame(
                    cursor.fetchall(), columns=["column_name", "data_type"]
                )
