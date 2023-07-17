import sqlite3

_DATABASE_NAME = "wikicache.db"

class AbstractDAO:
    def __init__(self):
        self._conn = sqlite3.connect(_DATABASE_NAME)
        self._cur = self._conn.cursor()

    def close(self):
        self._cur.close()
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.close()

class CategoriesDAO(AbstractDAO):
    def create_tables(self):
        self._cur.execute("DROP TABLE IF EXISTS categories")
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS categories
                (category_id INTEGER PRIMARY KEY, title TEXT NOT NULL)
        """)
        self._cur.execute("DROP TABLE IF EXISTS category_subcategories")
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS category_subcategories (
                category_subcategory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                subcategory_id INTEGER NOT NULL
            )
        """)
        self._conn.commit()

    def update_category(self, category):
        self._cur.execute(
            "INSERT INTO categories (category_id, title) VALUES(?, ?)",
            (category["category_id"], category["title"])
        )
        self._conn.commit()


    def update_category_subcategory(self, category, subcategory):
        self._cur.execute(
            "INSERT INTO category_subcategories (category_id, subcategory_id) VALUES(?, ?)",
            (category["category_id"], subcategory["category_id"])
        )
        self._conn.commit()

    def exists_category(self, category):
        category_id = category["category_id"]
        
        self._cur.execute(
            "SELECT * FROM categories WHERE category_id=?",
            (category_id,)
        )
        return bool(self._cur.fetchone())

    def read_category_ids(self):
        category_ids = []

        self._cur.execute("SELECT category_id FROM categories")
        category_id_tuples = self._cur.fetchall()
        for category_id_tuple in category_id_tuples:
            category_ids.append(category_id_tuple[0])
        
        return category_ids


class CategoryPagesDAO(AbstractDAO):
    def create_tables(self):
        self._cur.execute("DROP TABLE IF EXISTS category_pages")
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS category_pages (
                category_page_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                page_id INTEGER NOT NULL
            )
        """)
        self._conn.commit()

    def update_category_pages(self, category_id, page_id):
        self._cur.execute(
            "INSERT INTO category_pages (category_id, page_id) VALUES(?, ?)",
            (category_id, page_id)
        )
        self._conn.commit()

    def read_page_ids(self):
        page_ids = []        

        self._cur.execute("SELECT DISTINCT page_id FROM category_pages")
        page_id_tuples = self._cur.fetchall()
        for page_id_tuple in page_id_tuples:
            page_ids.append(page_id_tuple[0])
        
        return page_ids

class PagesDAO(AbstractDAO):
    def create_tables(self):
        self._cur.execute("DROP TABLE IF EXISTS pages")
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                page_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                url TEXT NOT NULL,
                description TEXT
            )
        """)
        self._cur.execute("DROP TABLE IF EXISTS page_images")
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS page_images (
                page_image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER NOT NULL,
                image_title TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def update_page(self, page):
        self._cur.execute(
            "INSERT INTO pages (page_id, title, latitude, longitude, url) VALUES(?, ?, ?, ?, ?)",
            (page["page_id"], page["title"], page["latitude"], page["longitude"], page["url"]));

        if "description" in page:
            self._cur.execute(
                "UPDATE pages SET description = ? WHERE page_id = ?",
                (page["description"], page["page_id"])
            )

        self._conn.commit()

    def update_page_image(self, page, image_title):
        self._cur.execute(
            "INSERT INTO page_images (page_id, image_title) VALUES(?, ?)",
            (page["page_id"], image_title)
        )
        self._conn.commit()

    def read_image_titles(self):
        image_titles = []

        self._cur.execute("SELECT DISTINCT image_title FROM page_images")
        page_image_tuples = self._cur.fetchall()
        for page_image_tuple in page_image_tuples:
            image_titles.append(page_image_tuple[0])

        return image_titles

class ImagesDAO(AbstractDAO):
    def create_tables(self):
        self._cur.execute("DROP TABLE IF EXISTS images")
        self._cur.execute("""
            CREATE TABLE IF NOT EXISTS images (
                image_title TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                author TEXT NOT NULL,
                license TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def update_image(self, image):
        self._cur.execute(
            "INSERT INTO images (image_title, url, author, license) VALUES(?, ?, ?, ?)",
            (image["image_title"], image["url"], image["author"], image["license"])
        )
        self._conn.commit()

    def read_images(self):
        images = []

        self._cur.execute("SELECT DISTINCT * FROM images")
        image_tuples = self._cur.fetchall()
        for image_tuple in image_tuples:
            image = {
                "image_title": image_tuple[0],
                "url": image_tuple[1],
                "author": image_tuple[2],
                "license": image_tuple[3],
            }
            images.append(image)

        return images

