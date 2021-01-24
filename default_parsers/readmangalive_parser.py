from bs4 import BeautifulSoup
from requests import Session
from typing import List
from .abstract_parser import AbstractParser


class ReadMangaLiveParser:
    def __init__(self, session=None, **kwargs):
        if session is None:
            session = Session()
        self.session = session

    def get_chapter_list(self, url, **kwargs):
        response = self.session.get(url)
        dom = BeautifulSoup(response.json())
        dom.select_one('.btn-block').get_attribute_list()

    def get_chapter_pages(self, *args, **kwargs) -> List[str]:
        pass

    def search(self, query, *args, **kwargs):
        url = "https://readmanga.live/search/suggestion"
        try:
            response = self.session.get(url, data={
                'query': query,
            })
            if not response.ok:
                raise Exception(f"Response failed with status code {response.status_code}")
            json_data = response.json()
            return json_data
        except Exception as e:
            print(e)
            return {
                'query': None,
                'suggestions': [],
            }
