import requests
from bs4 import BeautifulSoup
import datetime
from zoneinfo import ZoneInfo


def pray_time(a):
    while True:
        current_time = datetime.datetime.now(tz=ZoneInfo("Asia/Tashkent")).strftime('%H:%M:%S')
        date = datetime.date.today()
        url = f'https://islom.uz/vaqtlar/{a}/{datetime.datetime.now().month}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.find_all('tr', class_='juma bugun'):
            city_href = soup.find_all('tr', class_='juma bugun')
        else:
            city_href = soup.find_all('tr', class_='p_day bugun')

        for i in city_href:
            table_data = i.find_all('td')
            data = [j.text for j in table_data]
            kun = data[2]
            tong = data[3]
            quyosh = data[4]
            pewn = data[5]
            asr = data[6]
            shom = data[7]
            xufton = data[8]

        dict = {"27": 'Тошкент', '37': 'Фарғона', '1': 'Андижон', '15': 'Наманган',
                '4': "Бухоро", '9': 'Жиззах', '25': 'Қарши', '16': 'Нукус',
                '14': 'Навоий', '18': 'Самарқанд', '21': 'Хива', '5': 'Гулистон', '6': 'Денов',
                '26': 'Қўқон', '13': 'Марғилон', '3': 'Бишкек', '19': 'Туркистон',
                '61': 'Зарафшон', '20': 'Ўш', '78': 'Урганч', '74': 'Термиз'}
        if a in dict.keys():
            y = dict[a]
        text = f'⌛️<b>Намоз вақтлари <u><i>{y.upper()}</i></u> шаҳри бўйича:</b>\n\n' \
               f'==============================\n' \
               f'🏙<b>Тонг(Саҳарлик):</b>      《<i>{tong}</i>》\n' \
               f'🌃<b>Куёш:</b>                         《<i>{quyosh}</i>》\n' \
               f'-----------------------------------------------------\n' \
               f'🏙<b>Бомдод:</b>                    《<i>{tong}</i>》\n' \
               f'🌇<b>Пешин:</b>                     《<i>{pewn}</i>》\n' \
               f'🌆<b>Аср:</b>                            《<i>{asr}</i>》\n' \
               f'🏙<b>Шом(Ифтор):</b>          《<i>{shom}</i>》\n' \
               f'🌃<b>Хуфтон:</b>                     《<i>{xufton}</i>》\n' \
               f'==============================\n\n' \
               f'📅 <u><b>Сана:</b> <i> {date}</i></u>    | 📍<u><b>Кун:</b> <i>{kun}</i></u>\n⏱<u><b> Вақт:</b> <i> {current_time}</i></u>         |  🔗<u><b> Манбаа:</b>  <i>islom.uz</i></u>\n<u><b>🤖Бот:</b>  <i>@namozvaqtlarirobot</i></u>'
        return text
