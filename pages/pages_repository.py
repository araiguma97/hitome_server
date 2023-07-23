from typing import Generator

from repository import Repository
from wiki_data_source import WikiDataSource
from categories.category_pages_dao import CategoryPagesDAO
from pages.pages_dao import PagesDAO
from pages.texts_dao import TextsDAO
from pages.page import Page

class PagesRepository(Repository):

    def _create_daos(self) -> None:
        self._wiki_data_source = WikiDataSource()
        self._category_pages_dao = CategoryPagesDAO(self._conn)
        self._pages_dao = PagesDAO(self._conn)
        self._texts_dao = TextsDAO(self._conn)

    def update(self) -> None:
        self._update_pages()
        #self._update_texts()

    def get(self) -> Generator[Page, None, None]:
        return self._pages_dao.get_pages()

    def _update_pages(self) -> None:
        self._pages_dao.create_tables()

        for page_ids in self._category_pages_dao.get_page_ids(50):
            for page in self._wiki_data_source.get_page(page_ids):
                print("Updating page \"" + page.title + "\"")
                self._pages_dao.insert_page(page)
    
    def _update_texts(self) -> None:
        self._texts_dao.create_tables()

        for page_ids in self._category_pages_dao.get_page_ids(1):
            page_id = page_ids[0]
            text = self._wiki_data_source.get_text(page_id)
            print("Updating text (page_id=" + str(page_id) + ")")
            self._texts_dao.insert_text(page_id, text)
