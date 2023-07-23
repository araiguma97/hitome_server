from contextlib import closing
from sqlite3 import Connection
from typing import Generator
from images.image import Image


class ImagesDAO:

    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    def create_tables(self) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS images")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS images (
                    image_title TEXT PRIMARY KEY,
                    source      TEXT NOT NULL,
                    author      TEXT NOT NULL,
                    license     TEXT NOT NULL
                )
                """
            )
        self._conn.commit()

    def insert_image(self, image: Image) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO images (image_title, source, author, license) VALUES(?, ?, ?, ?)",
                (image.image_title, image.source, image.author, image.license)
            )
        self._conn.commit()

    def get_images(self) -> Generator[Image, None, None]:
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT * FROM images")
            while True:
                image_tuple = cur.fetchone()
                if not image_tuple:
                    break
                yield Image(
                    image_title = image_tuple[0],
                    source      = image_tuple[1],
                    author      = image_tuple[2],
                    license     = image_tuple[3]
                )

    def get_image_by_title(self, image_title):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT * FROM images WHERE image_title = ?", (image_title,))
            image_tuple = cur.fetchone()
            if not image_tuple:
                return None
            return Image(
                image_title = image_tuple[0],
                source      = image_tuple[1],
                author      = image_tuple[2],
                license     = image_tuple[3],
            )
