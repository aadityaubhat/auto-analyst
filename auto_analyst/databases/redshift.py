from auto_analyst.databases.base import BaseDatabase
import redshift_connector


class Redshift(BaseDatabase):
    """Class to interact with Redshift
    Attributes:
        host (str): Hostname of the Redshift cluster
        port (int): Port number of the Redshift cluster
        user (str): Username to connect to the Redshift cluster
        password (str): Password to connect to the Redshift cluster
    """

    def __init__(self, host, port, user, password, database):
        """Initialize Redshift

        Args:
            host (str): Hostname of the Redshift cluster
            port (int): Port number of the Redshift cluster
            user (str): Username to connect to the Redshift cluster
            password (str): Password to connect to the Redshift cluster
            database (str): Database name"""
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
        """Run query
        Args:
            query (str): Query to be executed
        Returns:
            pd.DataFrame: Dataframe containing the results of the query"""
        self.cursor.execute(query)
        return self.cursor.fetch_dataframe()
