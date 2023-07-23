from typing import Optional

from repository import Repository
from pages.pages_dao import PagesDAO
from pages.page import Page
from images.images_dao import ImagesDAO
from images.image import Image
from wiki_data_source import WikiDataSource


class ImagesRepository(Repository):

    def _create_daos(self) -> None:
        self._wiki_data_source = WikiDataSource()
        self._pages_dao = PagesDAO(self._conn)
        self._images_dao = ImagesDAO(self._conn)

    def update(self) -> None:
        self._images_dao.create_tables()

        for image_titles in self._pages_dao.get_image_titles(50):
            for image in self._wiki_data_source.get_image_titles(image_titles):
                print("Updating image \"" + image.image_title + "\"")
                self._images_dao.insert_image(image)
    
    def get_page_image(self, page: Page) -> Optional[Image]:
        if page.image_title is "":
            return None
        else:
            return self._images_dao.get_image_by_title(page.image_title)
