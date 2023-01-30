import json
from .models import Time
import requests
from bs4 import BeautifulSoup
from zoneinfo import ZoneInfo
from datetime import datetime

dict = {"27": 'Тошкент', '37': 'Фарғона', '1': 'Андижон', '15': 'Наманган',
        '4': "Бухоро", '9': 'Жиззах', '25': 'Қарши', '16': 'Нукус',
        '14': 'Навоий', '18': 'Самарқанд', '21': 'Хива', '5': 'Гулистон', '6': 'Денов',
        '26': 'Қўқон', '13': 'Марғилон', '3': 'Бишкек', '19': 'Туркистон',
        '61': 'Зарафшон', '20': 'Ўш', '78': 'Урганч', '74': 'Термиз'}


def pray_time(a):
    Time.objects.create(city_id=a, city=dict[a])
    # time = Time.objects.get(city_id=a)
    # current_time = datetime.now(tz=ZoneInfo("Asia/Tashkent")).strftime('%H:%m')
    # time.updated_time = current_time
    # time.save()
    # date = datetime.now().date()
    # if time.updated_date != datetime.now().date():
    #     url = f'https://islom.uz/vaqtlar/{a}/{datetime.now().month}'
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     if soup.find_all('tr', class_='juma bugun'):
    #         city_href = soup.find_all('tr', class_='juma bugun')
    #     else:
    #         city_href = soup.find_all('tr', class_='p_day bugun')
    #
    #     for i in city_href:
    #         table_data = i.find_all('td')
    #         data = [j.text for j in table_data]
    #         kun = data[2]
    #         tong = datetime.strptime(data[3], '%H:%M').strftime('%H:%M')
    #         quyosh = datetime.strptime(data[4], '%H:%M').strftime('%H:%M')
    #         pewn = datetime.strptime(data[5], '%H:%M').strftime('%H:%M')
    #         asr = datetime.strptime(data[6], '%H:%M').strftime('%H:%M')
    #         shom = datetime.strptime(data[7], '%H:%M').strftime('%H:%M')
    #         xufton = datetime.strptime(data[8], '%H:%M').strftime('%H:%M')
    #         time.kun = kun
    #         time.tong = tong
    #         time.quyosh = quyosh
    #         time.peshin = pewn
    #         time.asr = asr
    #         time.shom = shom
    #         time.xufton = xufton
    #         time.date = date
    #         time.updated_time = current_time
    #         time.updated_date = date
    #         time.save()
    #         text = f'⌛️<b>Намоз вақтлари <u><i>{dict[a]}</i></u> шаҳри бўйича:</b>\n\n' \
    #                f'==============================\n' \
    #                f'🏙<b>Тонг(Саҳарлик):</b>      《<i>{tong}</i>》\n' \
    #                f'🌃<b>Куёш:</b>                         《<i>{quyosh}</i>》\n' \
    #                f'-----------------------------------------------------\n' \
    #                f'🏙<b>Бомдод:</b>                    《<i>{tong}</i>》\n' \
    #                f'🌇<b>Пешин:</b>                     《<i>{pewn}</i>》\n' \
    #                f'🌆<b>Аср:</b>                            《<i>{asr}</i>》\n' \
    #                f'🏙<b>Шом(Ифтор):</b>          《<i>{shom}</i>》\n' \
    #                f'🌃<b>Хуфтон:</b>                     《<i>{xufton}</i>》\n' \
    #                f'==============================\n\n' \
    #                f'📅 <u><b>Сана:</b> <i> {date}</i></u>    | 📍<u><b>Кун:</b> <i>{kun}</i></u>\n⏱<u><b> Вақт:</b> <i> {current_time}</i></u>         |  🔗<u><b> Манбаа:</b>  <i>islom.uz</i></u>\n<u><b>🤖Бот:</b>  <i>@namozvaqtlarirobot</i></u>'
    #         return text
    #
    # else:
    #     text = f'⌛️<b>Намоз вақтлари <u><i>{time.city}</i></u> шаҳри бўйича:</b>\n\n' \
    #            f'==============================\n' \
    #            f'🏙<b>Тонг(Саҳарлик):</b>      《<i>{time.tong.strftime("%H:%M")}</i>》\n' \
    #            f'🌃<b>Куёш:</b>                         《<i>{time.quyosh.strftime("%H:%M")}</i>》\n' \
    #            f'-----------------------------------------------------\n' \
    #            f'🏙<b>Бомдод:</b>                    《<i>{time.tong.strftime("%H:%M")}</i>》\n' \
    #            f'🌇<b>Пешин:</b>                     《<i>{time.peshin.strftime("%H:%M")}</i>》\n' \
    #            f'🌆<b>Аср:</b>                            《<i>{time.asr.strftime("%H:%M")}</i>》\n' \
    #            f'🏙<b>Шом(Ифтор):</b>          《<i>{time.shom.strftime("%H:%M")}</i>》\n' \
    #            f'🌃<b>Хуфтон:</b>                     《<i>{time.xufton.strftime("%H:%M")}</i>》\n' \
    #            f'==============================\n\n' \
    #            f'📅 <u><b>Сана:</b> <i> {time.date}</i></u>    | 📍<u><b>Кун:</b> <i>{time.kun}</i></u>\n⏱<u><b> Вақт:</b> <i> {time.updated_date}</i></u>         |  🔗<u><b> Манбаа:</b>  <i>islom.uz</i></u>\n<u><b>🤖Бот:</b>  <i>@namozvaqtlarirobot</i></u>'
    #     return text


def surahs(sura):
    with open('./data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data[sura]
