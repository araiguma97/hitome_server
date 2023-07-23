from contextlib import closing
from sqlite3 import Connection
from typing import Generator

from categories.category import Category


class CategoriesDAO:

    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def create_tables(self) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS categories")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY,
                    title       TEXT    NOT NULL
                )
                """
            )
        self._conn.commit()

    def insert_category(self, category: Category) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO categories (category_id, title) VALUES(?, ?)",
                (category.category_id, category.title)
            )
        self._conn.commit()

    def exists_category(self, category: Category) -> bool:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM categories WHERE category_id = ?",
                (category.category_id,)
            )
            return bool(cur.fetchall())

    def get_category_ids(self) -> Generator[int, None, None]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT category_id FROM categories")
            while True:
                category_id_tuple = cur.fetchone()
                if not category_id_tuple:
                    break
                yield category_id_tuple[0]

    def get_category_by_id(self, category_id) -> Category:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM categories WHERE category_id = ?",
                (category_id,)
            )
            category_tuple = cur.fetchone()
            return Category(
                category_id = category_tuple[0],
                title       = category_tuple[1]
            )
