import datetime
from requests import Session
from typing import List


class IMangaChapterPage:

    @property
    def url(self):
        raise NotImplementedError()

    @property
    def number(self) -> int:
        raise NotImplementedError()


class IChapter:

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def description(self) -> str:
        raise NotImplementedError()

    @property
    def published_at(self) -> datetime.datetime:
        raise NotImplementedError()

    @property
    def pages_count(self) -> int:
        raise NotImplementedError()

    @property
    def pages_list(self) -> List[IMangaChapterPage]:
        raise NotImplementedError()


class IManga:

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def description(self) -> str:
        raise NotImplementedError()

    @property
    def entry_point(self) -> int:
        raise NotImplementedError()

    @property
    def volume_count(self) -> int:
        raise NotImplementedError()

    @property
    def chapter_count(self) -> str:
        raise NotImplementedError()

    @property
    def score(self) -> int:
        raise NotImplementedError()

    @property
    def max_score(self) -> str:
        raise NotImplementedError()

    @property
    def chapter_list(self) -> IChapter:
        raise NotImplementedError()

    @property
    def publishing_start(self) -> datetime.date:
        raise NotImplementedError()

    @property
    def publishing_end(self) -> datetime.date:
        raise NotImplementedError()

    @property
    def status(self) -> str:
        raise NotImplementedError()

    @property
    def last_chapter_published_at(self) -> datetime.date:
        raise NotImplementedError()

    @property
    def translator(self):
        raise NotImplementedError()


class AbstractParser:
    def __init__(self, *args, **kwargs):
        pass

    def get_manga_info(self, *args, **kwargs):
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
