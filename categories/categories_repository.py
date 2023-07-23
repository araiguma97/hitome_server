from typing import Generator

import utils
from wiki_data_source import WikiDataSource
from repository import Repository
from categories.category import Category
from categories.categories_dao import CategoriesDAO
from categories.category_pages_dao import CategoryPagesDAO
from pages.page import Page

class CategoriesRepository(Repository):

    def _create_daos(self) -> None:
        self._wiki_data_source  = WikiDataSource()
        self._categories_dao    = CategoriesDAO(self._conn)
        self._category_pages_dao = CategoryPagesDAO(self._conn)

    def update(self) -> None:
        self._update_categories()
        self._update_category_pages()

    def get_categories(self, page: Page) -> Generator[Category, None, None]:
        for category_id in self._category_pages_dao.get_category_id_by_page_id(page.page_id):
            yield self._categories_dao.get_category_by_id(category_id)

    def _update_categories(self) -> None:
        self._categories_dao.create_tables()
        for root_category_title in utils.load_json("root_categories.json"):
            root_category = self._wiki_data_source.get_category_by_title(root_category_title)
            if root_category is None:
                print("Root category \"" + root_category_title + "\" is not found")
                continue
            self._search_all_subcategories(root_category)

    def _search_all_subcategories(self, category: Category) -> None:
        if self._categories_dao.exists_category(category):
            return

        print("Updating category \"" + category.title + "\"")
        self._categories_dao.insert_category(category)

        subcategories = self._wiki_data_source.get_subcategories(category)
        for subcategory in subcategories:
            self._search_all_subcategories(subcategory)
    
    def _update_category_pages(self) -> None:
        self._category_pages_dao.create_tables()

        for category_id in self._categories_dao.get_category_ids():
            for page_id in self._wiki_data_source.get_page_id(category_id):
                print("Updating page (id=" + str(page_id) + ") of category (id=" + str(category_id) + ")")
                self._category_pages_dao.insert_category_pages(category_id, page_id)
