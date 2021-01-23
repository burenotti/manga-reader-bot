from requests import Session
from typing import List


class AbstractParser:
    def __init__(self, *args, **kwargs):
        pass

    def get_chapter_list(self, *args, **kwargs):
        pass

    def get_chapter_pages(self, *args, **kwargs) -> List[str]:
        pass

    def search(self, query, *args, **kwargs):
        pass


class SeleniumPoweredAbstractParser(AbstractParser):

    def __init__(self, driver, *args, **kwargs):
        super(SeleniumPoweredAbstractParser, self).__init__()
        self.driver = driver
