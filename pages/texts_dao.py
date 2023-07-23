from contextlib import closing
from sqlite3 import Connection
from typing import Generator

from pages.page import Page


class TextsDAO:

    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def create_tables(self) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS texts")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS texts (
                    page_id INTEGER PRIMARY KEY,
                    text    TEXT    NOT NULL
                )
                """
            )
        self._conn.commit()

    def insert_text(self, page_id: int, text: str) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO texts (page_id, text) VALUES(?, ?)",
                (page_id, text)
            )
        self._conn.commit()
