import os
import json
from .abstract_parser import SeleniumPoweredAbstractParser
from selenium import webdriver
from typing import List


class MangalibParser(SeleniumPoweredAbstractParser):
    DOMAIN = 'mangalib.me'
    START_READ_CSS_SELECTOR = '.media-sidebar__buttons>a[href]'
    CHAPTER_PATH_TEMPLATE = '{path}/v{volume}/c{chapter}'
    SERVER_TEMPLATE = '{server}/{url}{img}'
    CHAPTER_PAGE_SELECTOR = 'script#pg'

    def __init__(self, driver: webdriver.Chrome, *args, **kwargs):
        super(MangalibParser, self).__init__(driver)

    def get_chapter_list(self, path: str):
        url = self.get_first_chapter_url(path)
        self.driver.get(url)
        return self.parse_window_data()

    def parse_window_data(self):
        return self.driver.execute_script('return window.__DATA__')

    def parse_window_info(self):
        return self.driver.execute_script('return window.__info')

    def parse_window_pg(self):
        return self.driver.execute_script('return window.__pg')

    def get_first_chapter_url(self, path: str):
        self.driver.get(self.build_url(path=path))
        element = self.driver.find_element_by_css_selector(self.START_READ_CSS_SELECTOR)
        return element.get_attribute('href')

    def get_chapter_pages(self, slug, volume, chapter, *args, **kwargs) -> List[str]:
        chapter_url = self.build_url(path=self.CHAPTER_PATH_TEMPLATE.format(path=slug,
                                                                       volume=volume,
                                                                       chapter=chapter))
        self.driver.get(chapter_url)
        info = self.parse_window_info()
        pages = self.parse_window_pg()
        server = info['servers'][info['img']['server']]
        page_urls = []
        for page_info in pages:
            url = self.SERVER_TEMPLATE.format(
                server=server,
                url=info['img']['url'],
                img=page_info['u'].strip('/'),
            )
            page_urls.append(url)
        return page_urls

    def search(self, query, *args, **kwargs):
        try:
            self.driver.get(self.build_url(path='search', params={
                'type': 'manga',
                'q': query,
            }))
            raw_text = self.driver.find_element_by_css_selector('pre').text
            deserialized_json = json.loads(raw_text)
            return deserialized_json
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def build_url(proto='https', domain=DOMAIN, path='', params=None):
        query_string = MangalibParser.join_query_params(params)
        path = path.strip('/')
        return f"{proto}://{domain}/{path}/?{query_string}"

    @staticmethod
    def join_query_params(params=None):
        if params is None:
            params = {}
        return '&'.join([f"{key}={value}" for key, value in params.items()])
