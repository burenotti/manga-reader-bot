from telegraph import Telegraph
from requests import Session
from bs4 import BeautifulSoup


class TelegraphPublisher:

    def __init__(self, access_token=None, telegraph=None):
        if telegraph is not None:
            self.telegraph = telegraph
        else:
            self.telegraph = Telegraph(access_token=access_token)

    def publish(self, title, image_list, author_name='', author_url=''):
        dom = BeautifulSoup(features='html.parser')
        for image_url in image_list:
            tag = dom.new_tag('img', attrs={'src': image_url})
            dom.append(tag)
        response = self.telegraph.create_page(title=title,
                                              html_content=''.join(map(str, dom.contents)),
                                              author_url=author_url,
                                              author_name=author_name)
        return response
