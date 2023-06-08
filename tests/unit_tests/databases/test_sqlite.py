import unittest
from flask import Flask
from auto_analyst.databases.sqlite import SQLLite


class TestSQLLite(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.db = SQLLite()

    def tearDown(self):
        self.ctx.pop()
        with self.app.app_context():
            self.db.close_connection()

    def test_list_tables(self):
        with self.app.app_context():
            table_list = self.db.get_tables()
            self.assertEqual(len(table_list), 11)
            self.assertEqual(
                sorted(table_list["table_name"].tolist()),
                [
                    "Album",
                    "Artist",
                    "Customer",
                    "Employee",
                    "Genre",
                    "Invoice",
                    "InvoiceLine",
                    "MediaType",
                    "Playlist",
                    "PlaylistTrack",
                    "Track",
                ],
            )

    def test_get_schema(self):
        with self.app.app_context():
            schema = self.db.get_schema("Album")
            self.assertEqual(len(schema), 3)
            self.assertEqual(
                sorted(schema["name"].tolist()), ["AlbumId", "ArtistId", "Title"]
            )

    def test_run_query(self):
        with self.app.app_context():
            result = self.db.run_query("select * from Invoice")
            self.assertEqual(len(result), 412)


# if this file is run directly, run the tests
if __name__ == "__main__":
    unittest.main()
