from flask import g
from auto_analyst.databases.base import BaseDatabase
import sqlite3
import pandas as pd


class SQLLite(BaseDatabase):
    """Class for SQLLite
    Attributes:
        db_path (str): Path to the SQLLite database"""

    def __init__(self, db_path=None):
        """Initialize SQLLite
        Args:
            db_path (str): Path to the SQLLite database"""
        if db_path is None:
            db_path = "auto_analyst/databases/sample_data/chinook.sqlite"
        self.db_path = db_path

    def get_cursor(self) -> sqlite3.Cursor:
        """Connect to SQLLite if not already connected
        Returns:
            sqlite3.Cursor: Cursor object"""
        if "db" not in g:
            g.db = sqlite3.connect(self.db_path)
            g.cursor = g.db.cursor()
        return g.cursor

    def close_connection(self) -> None:
        """Disconnect from SQLLite"""
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def run_query(self, query: str) -> pd.DataFrame:
        """Run query
        Args:
            query (str): Query to be executed
        Returns:
            pd.DataFrame: Dataframe containing the results of the query"""
        if "db" not in g:
            self.get_cursor()
        return pd.read_sql_query(query, g.db)

    def get_tables(self) -> pd.DataFrame:
        """Get all tables"""
        return self.run_query(
            "select name as table_name from sqlite_master where type='table'"
        )

    def get_schema(self, table_name: str):
        """Get schema for the given table
        Args:
            table_name (str): Name of the table
        Returns:
            pd.DataFrame: Dataframe containing table schema"""
        return self.run_query(f"PRAGMA table_info({table_name})")
