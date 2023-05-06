from auto_analyst.databases.sqlite import SQLLite
import pytest


@pytest.fixture(scope="module")
def db():
    db = SQLLite()
    yield db
    db.disconnect()


def test_list_tables(db):
    table_list = db.list_tables()
    assert len(table_list) == 11
    assert sorted(table_list["table_name"].tolist()) == [
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
    ]


def test_get_schema(db):
    schema = db.get_schema("Album")
    assert len(schema) == 3
    assert sorted(schema["name"].tolist()) == ["AlbumId", "ArtistId", "Title"]


def test_run_query(db):
    assert len(db.run_query("select * from Invoice")) == 412
