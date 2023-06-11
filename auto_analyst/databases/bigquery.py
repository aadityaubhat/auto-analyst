from google.cloud import bigquery
from google.oauth2 import service_account
from typing import List
import pandas as pd
from auto_analyst.databases.base import BaseDatabase


class BigQueryDatabase(BaseDatabase):
    """Implementation of BaseDatabase for BigQuery"""

    def __init__(self, project_id: str, credentials_path: str):
        """Initialize BigQueryDatabase with project_id and path to service account credentials"""
        self.project_id = project_id
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        self.client = bigquery.Client(
            credentials=self.credentials, project=self.project_id
        )

    def run_query(self, query: str) -> pd.DataFrame:
        """Run query using BigQuery"""
        query_job = self.client.query(query)  # API request
        return query_job.to_dataframe()

    def get_tables(self) -> List[str]:
        """List tables in BigQuery"""
        tables = list(self.client.list_tables(self.project_id))
        return [table.table_id for table in tables]

    def get_schema(self, table_name: str) -> List[bigquery.SchemaField]:
        """Get schema for the given table in BigQuery"""
        table = self.client.get_table(table_name)  # API request
        return table.schema
