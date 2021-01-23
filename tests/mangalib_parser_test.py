import os
import json
from default_parsers import MangalibParser
from selenium.webdriver import ChromeOptions, Chrome
from environment import SELENIUM_WEBDRIVER_DIR

os.environ['Path'] += ";{};".format(os.path.join(SELENIUM_WEBDRIVER_DIR))
options = ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-javascript")
driver = Chrome(options=options)
parser = MangalibParser(driver)
result = parser.search('Jojo')
slug = result[0]['slug']
chapter_list = parser.get_chapter_list(slug)['chapters']
chapter = chapter_list[-1]
print(*parser.get_chapter_pages(slug, str(chapter['chapter_volume']), chapter['chapter_number']), sep='\n')
