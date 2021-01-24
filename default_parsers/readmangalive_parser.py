import json
from bs4 import BeautifulSoup
from requests import Session
from typing import List
from .abstract_parser import AbstractParser


class ReadMangaLiveParser:

    domain = 'https://readmanga.live/{link}'
    rejected = ['Автор', 'Переводчик']

    def __init__(self, session=None, **kwargs):
        if session is None:
            session = Session()
        self.session = session

    def get_entry_point(self, link):
        url = self.domain.format(link=link.lstrip('/'))
        entry_point = None
        try:
            response = self.session.get(url)
            dom = BeautifulSoup(response.text, features="html.parser")
            entry_point = dom.select_one('.btn-block').get_attribute_list('href')[0]
        except Exception as e:
            print(e)
        return entry_point

    def get_chapter_list(self, link=None, entry_point=None, **kwargs):
        if link is None and entry_point is None:
            raise ValueError("You must specify either link or entry_point")
        elif entry_point is None:
            entry_point = self.get_entry_point(link)
            if entry_point is None:
                raise ValueError("Attempt to restore entry point from link has been failed")
        url = self.domain.format(link=entry_point)
        response = self.session.get(url)
        chapter_list = []
        if response.ok:
            dom = BeautifulSoup(response.text, features="html.parser")
            options = dom.select('select>option')
            chapter_list = [{
                'entry_point': opt.get_attribute_list('value')[0],
                'name': opt.get_text(),
            } for opt in options]
        return chapter_list

    def get_chapter_pages(self, entry_point: str, **kwargs) -> List[str]:
        url = self.domain.format(link=entry_point)
        response = self.session.get(url)
        pages = []
        if response.ok:
            start_token = 'rm_h.init('
            start = response.text.find(start_token) + len(start_token)
            end = response.text.find(');', start)
            text = '[' + response.text[start:end] + ']'
            text = text.replace("'", '"')
            pages_info = json.loads(text)[0]
            pages = [p[0] + p[2] for p in pages_info]
        return pages

    def search(self, query, *args, **kwargs):
        url = self.domain.format(link="search/suggestion")
        try:
            response = self.session.post(url, data={
                'query': query,
            })
            if not response.ok:
                raise Exception(f"Response failed with status code {response.status_code}")
            json_data = response.json()
            json_data['suggestions'] = [sug for sug in json_data['suggestions'] if sug not in self.rejected]
            return json_data
        except Exception as e:
            print(e)
            return {
                'query': None,
                'suggestions': [],
            }
