import sqlite3

from backend.app.db.session import set_sqlite_pragma


def test_sqlite_foreign_keys_enabled():
    with sqlite3.connect(":memory:") as connection:
        set_sqlite_pragma(connection, None)
        assert connection.execute("PRAGMA foreign_keys").fetchone() == (1,)


def test_non_sqlite_connection_is_untouched():
    class OtherConnection:
        def cursor(self):
            raise AssertionError("SQLite PRAGMA must not reach another database")

    set_sqlite_pragma(OtherConnection(), None)
