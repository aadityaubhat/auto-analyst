from auto_analyst.databases.base import BaseDatabase
import redshift_connector


class Redshift(BaseDatabase):
    """Class for Redshift"""
    # Implement the abstract methods from BaseDatabase
    
    def __init__(self, host, port, user, password, database):
        """Initialize Redshift"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self._connect()
    
    def _connect(self):
        """Connect to Redshift"""
        self.connection = redshift_connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
    
    def _disconnect(self):
        """Disconnect from Redshift"""
        self.connection.close()

    def run_query(self, query: str):
        """Run query"""
        self.cursor.execute(query)
        return self.cursor.fetch_dataframe()
    
    def list_tables(self):
        """List tables"""
        return self.run_query("select * from pg_tables")
    
    def get_schema(self, table_name: str):
        """Get schema for the given table"""
        return self.run_query(f"select * from {table_name} limit 1")
    
    