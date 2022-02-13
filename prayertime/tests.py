import requests
from bs4 import BeautifulSoup


def timess(a):

    url1 = 'http://uzsmart.ru/namoz-vaqtlari/'
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.text, 'lxml')
    current_time = soup1.find('span', id='current_time').text  # current time
    date = soup1.find('h2', style='font-size: 24px; color: red').text[1:11] #current date

    url = f'https://islom.uz/vaqtlar/{a}/2'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
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
        # print(kun, tong, quyosh, pewn, asr, shom, xufton)

    dict = {"27": 'Тошкент', '37': 'Фарғона', '1': 'Андижон', '15': 'Наманган',
            '4': "Бухоро", '9': 'Жиззах', '25': 'Қарши', '16': 'Нукус',
            '14': 'Навоий', '18': 'Самарқанд', '21': 'Хива', '5': 'Гулистон', '6': 'Денов',
            '26': 'Қўқон', '13': 'Марғилон', '3': 'Бишкек', '19': 'Туркистон',
            '61': 'Зарафшон', '20': 'Ўш', '78': 'Урганч', '74': 'Термиз'}
    if a in dict.keys():
        y = dict[a]

    return f'⌛️<b>Намоз вақтлари <u><i>{y.upper()}</i></u> шаҳри бўйича:</b>\n==============================\n🏙<b>Тонг:</b>             <i>{tong}</i>🌃<b>Куёш:</b>          <i>{quyosh}</i>------------------------------\n🏙<b>Бомдод:</b>          <i>{tong}</i>🌇<b>Пешин:</b>         <i>{pewn}</i>🌆<b>Аср:</b>               <i>{asr}</i>🏙<b>Шом:</b>            <i>{shom}</i>🌃<b>Хуфтон:</b>            <i>{xufton}</i>==============================\n📅 <u><b>Сана:</b> <i>    {date}</i></u>  || ⏱<u><b> Вақт:</b> <i>    {current_time[0:5]}</i></u>'


timess(27)
