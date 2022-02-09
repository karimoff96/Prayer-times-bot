import requests
from bs4 import BeautifulSoup


def pray_time(a):
    if a == 'Toshkent':
        url = 'http://uzsmart.ru/namoz-vaqtlari/'
    else:
        url = f'http://uzsmart.ru/namoz-vaqtlari/shahar/{a}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    current_time = soup.find('span', id='current_time').text  # current time tayyor
    date = soup.find('h2', style='font-size: 24px; color: red').text[1:11]
    quotes = soup.find('table', style='font-size: 24px')
    part = quotes.find_all('tr', class_='item')
    tong = part[0].text[14:]  # tong/sahar +
    quyosh = part[1].text[8:]
    pewn = part[2].text[8:]
    asr = part[3].text[5:]
    shom = part[4].text[14:]
    xufton = part[5].text[8:]
    dict = {"Toshkent": 'Тошкент', 'Farg%60ona': 'Фарғона', 'Andijon': 'Андижон', 'Jambul': 'Наманган',
            'Buxoro': "Бухоро", 'Jizzax': 'Жиззах', 'Qarshi': 'Қарши', 'Nukus': 'Нукус', 'Navoiy': 'Навоий',
            'Samarqand': 'Самарқанд',
            'Xiva': 'Хива', 'Guliston': 'Гулистон', 'Denov': 'Сурхандарё'}
    if a in dict.keys():
        y = dict[a]

    return f'⌛️<b>Намоз вақтлари <u><i>{y.upper()}</i></u> шаҳри бўйича:</b>\n==============================\n🏙<b>Тонг:</b> <i>{tong}</i>🌃<b>Куёш:</b> <i>{quyosh}</i>------------------------------\n🏙<b>Бомдод:</b> <i>{tong}</i>\n🌇<b>Пешин:</b> <i>{pewn}</i>\n🌆<b>Аср:</b> <i>{asr}</i>\n🏙<b>Шом:</b> <i>{shom}</i>\n🌃<b>Хуфтон:</b> <i>{xufton}</i>\n==============================\n📅 <u><b>Сана:</b> <i>{date}</i></u>\n🔎<u><b>Вақт:</b> <i>{current_time}</i></u>'
