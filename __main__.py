from bs4 import BeautifulSoup
from default_parsers import ReadMangaLiveParser
from telebot import TeleBot, types
from environment import TELEGRAM_API_TOKEN, TELEGRAPH_API_TOKEN
from telegraph import Telegraph

bot = TeleBot(TELEGRAM_API_TOKEN)
telegraph_api = Telegraph(TELEGRAPH_API_TOKEN)
parser = ReadMangaLiveParser()

callbacks = {
    'last_callback': 0,
    'none': {},
}


def create_telegaph_page(title, entry_point):
    pages = parser.get_chapter_pages(entry_point)
    dom = BeautifulSoup('', features='html.parser')
    for img in pages:
        dom.append(dom.new_tag(name='img', attrs={
            'src': img
        }))
    return telegraph_api.create_page(title=title,
                                     html_content=''.join((str(x) for x in dom.children)))['url']


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    search_button = types.InlineKeyboardButton('Поиск', switch_inline_query_current_chat='')
    keyboard.add(search_button)
    bot.send_message(message.from_user.id, 'Используйте поиск', reply_markup=keyboard)


@bot.callback_query_handler(lambda q: True)
def get_next_chapter(query: types.CallbackQuery):
    print("replying for", query.data)
    uid = query.from_user.id
    entry_point = callbacks[query.data]['next_chapter']
    chapter_list = parser.get_chapter_list(entry_point=entry_point)
    index = [index for index, chapter in enumerate(chapter_list) if chapter['entry_point'].startswith(entry_point)][0]
    next_chapter = chapter_list[index - 1]
    callbacks['last_callback'] += 1
    cb = str(callbacks['last_callback'])
    callbacks[cb] = {
        'next_chapter': next_chapter['entry_point']
    }
    tg_page = create_telegaph_page(next_chapter['name'], entry_point)
    keyboard = types.InlineKeyboardMarkup()
    start_read = types.InlineKeyboardButton(text="Следующая глава",
                                            callback_data=cb)
    keyboard.add(start_read)
    bot.send_message(uid, text=tg_page, reply_markup=keyboard)


@bot.message_handler(content_types=['text'],
                     regexp=r'(https|http)://readmanga\.live/([^/]+)(/){0,1}$')
def get_manga_info(message):
    print(1)
    url = message.text
    info = parser.get_manga_info(url)
    ans_msg_text = (f"Название: {info['name']}\n"
                    f"Описание: {info['description']}\n"
                    f"Оценка: {info['score']}")
    cb = str(callbacks['last_callback'] + 1)
    callbacks[cb] = {
        'next_chapter': info['entry_point'],
    }
    callbacks['last_callback'] += 1
    keyboard = types.InlineKeyboardMarkup()
    start_read = types.InlineKeyboardButton(text="Начать читать",
                                            callback_data=cb)
    keyboard.add(start_read)
    if info['thumb_urls']:
        bot.send_photo(message.from_user.id,
                       caption=ans_msg_text,
                       photo=info['thumb_urls'][0],
                       reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id,
                         text=ans_msg_text,
                         reply_markup=keyboard)


@bot.message_handler(content_types=['text'],
                     regexp=r'(https|http)://readmanga\.live/[^/]+/(vol|v)\d+/(c|)\d+')
def get_manga_chapter(message):
    print("got manga chapter request")


@bot.inline_handler(lambda query: len(query.query) > 4)
def search_query(inline_query):
    results = parser.search(inline_query.query)
    answers = []
    for index, res in enumerate(results):
        url = f'https://readmanga.live{res["link"]}'
        ans = types.InlineQueryResultArticle(index,
                                             title=res['value'],
                                             thumb_url=res['thumbnail'],
                                             url=url,
                                             input_message_content=types.InputTextMessageContent(url),
                                             hide_url=True)
        answers.append(ans)
    bot.answer_inline_query(inline_query.id, answers)


def main():
    bot.polling(True, 0)


if __name__ == '__main__':
    main()
