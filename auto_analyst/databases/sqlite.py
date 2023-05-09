from auto_analyst.databases.base import BaseDatabase
import sqlite3
import pandas as pd


class SQLLite(BaseDatabase):
    """ "Class for SQLLite"""

    def __init__(self, db_path=None):
        """Initialize SQLLite"""
        if db_path is None:
            db_path = "auto_analyst/databases/sample_data/chinook.sqlite"
        self.db_path = db_path
        self.cursor = self._connect()

    def _connect(self):
        """Connect to SQLLite"""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()

    def disconnect(self):
        """Disconnect from SQLLite"""
        self.cursor.close()
        self.connection.close()

    def run_query(self, query: str):
        """Run query"""
        return pd.read_sql_query(query, self.connection)

    def list_tables(self):
        """List tables"""
        return self.run_query(
            "select name as table_name from sqlite_master where type='table'"
        )

    def get_schema(self, table_name: str):
        """Get schema for the given table"""
        return self.run_query(f"PRAGMA table_info({table_name})")
