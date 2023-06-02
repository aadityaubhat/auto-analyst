from flask import g
from auto_analyst.databases.base import BaseDatabase
import sqlite3
import pandas as pd


class SQLLite(BaseDatabase):
    """Class for SQLLite"""

    def __init__(self, db_path=None):
        """Initialize SQLLite"""
        if db_path is None:
            db_path = "auto_analyst/databases/sample_data/chinook.sqlite"
        self.db_path = db_path

    def get_cursor(self):
        """Connect to SQLLite if not already connected"""
        if "db" not in g:
            g.db = sqlite3.connect(self.db_path)
            g.cursor = g.db.cursor()
        return g.cursor

    def close_connection(self):
        """Disconnect from SQLLite"""
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def run_query(self, query: str):
        """Run query"""
        return pd.read_sql_query(query, g.db)

    def list_tables(self):
        """List tables"""
        return self.run_query(
            "select name as table_name from sqlite_master where type='table'"
        )

    def get_schema(self, table_name: str):
        """Get schema for the given table"""
        return self.run_query(f"PRAGMA table_info({table_name})")
