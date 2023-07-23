from contextlib import closing
from sqlite3 import Connection
from typing import Generator


class CategoryPagesDAO:

    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def create_tables(self) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS category_pagess")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS category_pages (
                    category_page_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id      INTEGER NOT NULL,
                    page_id          INTEGER NOT NULL
                )
                """
            )
        self._conn.commit()

    def insert_category_pages(self, category_id: int, page_id: int) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO category_pages (category_id, page_id) VALUES(?, ?)",
                (category_id, page_id)
            )
        self._conn.commit()

    def get_page_ids(self, n: int) -> Generator[list[int], None, None]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT page_id FROM category_pages")
            while True:
                page_id_tuples = cur.fetchmany(n)
                if not page_id_tuples:
                    break
                yield [page_id_tuple[0] for page_id_tuple in page_id_tuples]

    def get_category_id_by_page_id(self, page_id: int) -> list[int]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT category_id FROM category_pages WHERE page_id = ?", (page_id,))
            category_id_tuples = cur.fetchall()
            return [category_id_tuple[0] for category_id_tuple in category_id_tuples]
