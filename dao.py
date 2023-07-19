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
                    break;
                yield category_id_tuple[0]

    def find_category_by_id(self, category_id):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT * FROM categories WHERE category_id = ?", (category_id,))
            category_tuple = cur.fetchone()
            if not category_tuple:
                return None
            category = {
                "category_id": category_tuple[0],
                "title": category_tuple[1],
            }
            return category

class CategorySubcategoriesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
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

    def update_category_pages(self, category_id, page_id):
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

    def find_category_id_by_page_id(self, page_id):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT category_id FROM category_pages WHERE page_id = ?", (page_id,))
            category_id_tuples = cur.fetchall()
            return [category_id_tuple[0] for category_id_tuple in category_id_tuples]

class PagesDAO(AbstractDAO):
    def create_tables(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("DROP TABLE IF EXISTS pages")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pages (
                    page_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    latitude REAL,
                    longitude REAL,
                    description TEXT,
                    image_title TEXT,
                    text TEXT
                )
            """)
        self._conn.commit()

    def create_page(self, page):
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO pages (page_id, title, url) VALUES(?, ?, ?)",
                (page["page_id"], page["title"], page["url"])
            )

            if "latitude" in page:
                cur.execute(
                    "UPDATE pages SET latitude = ? WHERE page_id = ?",
                    (page["latitude"], page["page_id"])
                )

            if "longitude" in page:
                cur.execute(
                    "UPDATE pages SET longitude = ? WHERE page_id = ?",
                    (page["longitude"], page["page_id"])
                )

            if "description" in page:
                cur.execute(
                    "UPDATE pages SET description = ? WHERE page_id = ?",
                    (page["description"], page["page_id"])
                )

            if "image_title" in page:
                cur.execute(
                    "UPDATE pages SET image_title = ? WHERE page_id = ?",
                    (page["image_title"], page["page_id"])
                )
        self._conn.commit()

    def update_page_text(self, page):
        with closing(self._conn.cursor()) as cur:
            if "text" in page:
                cur.execute(
                    "UPDATE pages SET text = ? WHERE page_id = ?",
                    (page["text"], page["page_id"])
                )
        self._conn.commit()

    def read_image_titles(self, n):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT DISTINCT image_title FROM pages WHERE image_title IS NOT NULL")
            while True:
                image_title_tuples = cur.fetchmany(n)
                if not image_title_tuples:
                    break
                yield [image_title_tuple[0] for image_title_tuple in image_title_tuples]

    def read_place_pages(self):
        with closing(self._conn.cursor()) as cur:
            cur.execute("""
                SELECT page_id, title, url, latitude, longitude, description, image_title FROM pages
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)
            while True:
                page_tuple = cur.fetchone()
                if not page_tuple:
                    break
                page = {
                    "page_id": page_tuple[0],
                    "title": page_tuple[1],
                    "url": page_tuple[2],
                    "latitude": page_tuple[3],
                    "longitude": page_tuple[4],
                }

                if page_tuple[5]:
                    page["description"] = page_tuple[5]

                if page_tuple[6]:
                    page["image_title"] = page_tuple[6]

                yield page

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
            while True:
                image_tuple = cur.fetchone()
                if not image_tuple:
                    break
                image = {
                    "image_title": image_tuple[0],
                    "url": image_tuple[1],
                    "author": image_tuple[2],
                    "license": image_tuple[3],
                }
                yield image

    def find_image_by_title(self, image_title):
        with closing(self._conn.cursor()) as cur:
            cur.execute("SELECT * FROM images WHERE image_title = ?", (image_title,))
            image_tuple = cur.fetchone()
            if not image_tuple:
                return None
            image = {
                "image_title": image_tuple[0],
                "url": image_tuple[1],
                "author": image_tuple[2],
                "license": image_tuple[3],
            }
            return image
