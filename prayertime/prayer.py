import requests
from telebot import *


# if  x in dict.keys():


def pray_time(a):
    b = requests.get(f'https://api.pray.zone/v2/times/today.json?city={a}').json()['results']['datetime'][0]
    c = b["date"]["gregorian"]
    r = b["times"]
    dict = {"tashkent": 'Тошкент', 'fergama': 'Фарғона', 'andijan': 'Андижон', 'namangan': 'Наманган',
            'bukhara': "Бухоро",
            'jizzakh': 'Жиззах', 'qarshi': 'Қанши', 'nukus': 'Нукус', 'navoiy': 'Навоий', 'samarkand': 'Самарқанд',
            'urgench': 'Урганч', 'termiz': 'Термиз', 'khiva': 'Хива', 'gulistan': 'Гулистон',
            'zarafshan': 'Зарафшон',
            'margilan': 'Марғилон', 'kokand': 'Қўқон'}
    if a in dict.keys():
        y = dict[a]

    return f'⌛️<b>Намоз вақтлари <u><i>{y.upper()}</i></u> шаҳри бўйича:</b>\n==============================\n🏙<b>Тонг:</b> <i>{r["Fajr"]}</i>\n🌃<b>Куёш:</b> <i>{r["Sunrise"]}</i>\n------------------------------\n🏙<b>Бомдод:</b> <i>{r["Fajr"]}</i>\n🌇<b>Пешин:</b> <i>{r["Dhuhr"]}</i>\n🌆<b>Аср:</b> <i>{r["Asr"]}</i>\n🏙<b>Шом:</b> <i>{r["Maghrib"]}</i>\n🌃<b>Хуфтон:</b> <i>{r["Isha"]}</i>\n==============================\n📅 <u><b>Сана:</b> <i>{c}</i></u>\n🔎<u><b>Манбаа:</b> <i>PrayerTimes.date</i></u>'
