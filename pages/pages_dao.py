from contextlib import closing
from sqlite3 import Connection
from typing import Generator

from pages.page import Page


class PagesDAO:

    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def create_tables(self) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS pages")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS pages (
                    page_id     INTEGER PRIMARY KEY,
                    title       TEXT    NOT NULL,
                    source      TEXT    NOT NULL,
                    latitude    REAL,
                    longitude   REAL,
                    description TEXT,
                    image_title TEXT
                )
                """
            )
        self._conn.commit()

    def insert_page(self, page: Page) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO pages (page_id, title, source, latitude, longitude, description, image_title) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (page.page_id, page.title, page.source, page.latitude, page.longitude, page.description, page.image_title)
            )
        self._conn.commit()

    def get_image_titles(self, n: int) -> Generator[list[str], None, None]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT image_title FROM pages WHERE image_title IS NOT NULL")
            while True:
                image_title_tuples = cur.fetchmany(n)
                if not image_title_tuples:
                    break
                yield [image_title_tuple[0] for image_title_tuple in image_title_tuples]

    def get_pages(self) -> Generator[Page, None, None]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("""SELECT * FROM pages""")
            while True:
                page_tuple = cur.fetchone()
                if not page_tuple:
                    break
                yield Page(
                    page_id     = page_tuple[0],
                    title       = page_tuple[1],
                    source      = page_tuple[2],
                    latitude    = page_tuple[3],
                    longitude   = page_tuple[4],
                    description = page_tuple[5],
                    image_title = page_tuple[6]
                )
