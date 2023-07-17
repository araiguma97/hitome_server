import sqlite3
from contextlib import closing

class AbstractDAO:
    def __init__(self, conn):
        self._conn = conn

class CategoriesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS categories")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories
                    (category_id INTEGER PRIMARY KEY, title TEXT NOT NULL)
            """)
        self._conn.commit()

    def update_category(self, category):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO categories (category_id, title) VALUES(?, ?)",
                (category["category_id"], category["title"])
            )
        self._conn.commit()

    def exists_category(self, category):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM categories WHERE category_id=?",
                (category["category_id"],)
            )
            return bool(cur.fetchall())

    def read_category_ids(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT category_id FROM categories")
            while True:
                category_id_tuple = cur.fetchone()
                if not category_id_tuple:
                    break
                yield category_id_tuple[0]

class CategoriesSubcategoiesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS categories")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories
                    (category_id INTEGER PRIMARY KEY, title TEXT NOT NULL)
            """)
            cur.execute("DROP TABLE IF EXISTS category_subcategories")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS category_subcategories (
                    category_subcategory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    subcategory_id INTEGER NOT NULL
                )
            """)
        self._conn.commit()

    def update_category_subcategory(self, category, subcategory):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO category_subcategories (category_id, subcategory_id) VALUES(?, ?)",
                (category["category_id"], subcategory["category_id"])
            )
        self._conn.commit()

class CategoryPagesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS category_pages")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS category_pages (
                    category_page_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    page_id INTEGER NOT NULL
                )
            """)
        self._conn.commit()

    def update_category_page(self, category_id, page_id):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO category_pages (category_id, page_id) VALUES(?, ?)",
                (category_id, page_id)
            )
        self._conn.commit()

    def read_page_ids(self, n):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT page_id FROM category_pages")
            while True:
                page_id_tuples = cur.fetchmany(n)
                if not page_id_tuples:
                    break
                yield [page_id_tuple[0] for page_id_tuple in page_id_tuples]

class PagesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS pages")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pages (
                    page_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    url TEXT NOT NULL,
                    description TEXT,
                    image_title TEXT
                )
            """)
        self._conn.commit()

    def update_page(self, page):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO pages (page_id, title, url) VALUES(?, ?, ?)",
                (page["page_id"], page["title"], page["url"])
            )

            try:
                cur.execute(
                    "UPDATE pages SET description = ? WHERE page_id = ?",
                    (page["description"], page["page_id"])
                )
            except KeyError:
                pass

            try:
                cur.execute(
                    "UPDATE pages SET latitude = ?, longitude = ? WHERE page_id = ?",
                    (page["latitude"], page["longitude"], page["page_id"])
                )
            except KeyError:
                pass

            try:
                cur.execute(
                    "UPDATE pages SET image_title = ? WHERE page_id = ?",
                    (page["image_title"], page["page_id"])
                )
            except KeyError:
                pass
        self._conn.commit()

    def read_image_titles(self, n):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT image_title FROM pages WHERE image_title IS NOT NULL")
            while True:
                image_title_tuples = cur.fetchmany(n)
                if not image_title_tuples:
                    break
                yield [image_title_tuple[0] for image_title_tuple in image_title_tuples]

class ImagesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS images")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    image_title TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    author TEXT NOT NULL,
                    license TEXT NOT NULL
                )
            """)
        self._conn.commit()

    def update_image(self, image):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO images (image_title, url, author, license) VALUES(?, ?, ?, ?)",
                (image["image_title"], image["url"], image["author"], image["license"])
            )

        self._conn.commit()

    def read_images(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT * FROM images")
            image_tuples = cur.fetchall()
            for image_tuple in image_tuples:
                image = {
                    "image_title": image_tuple[0],
                    "url": image_tuple[1],
                    "author": image_tuple[2],
                    "license": image_tuple[3],
                }
                yield image

