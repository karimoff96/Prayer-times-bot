import requests
from bs4 import BeautifulSoup


def prayer_time(a):
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
    return date
print(prayer_time('Andijon'))
    # urls = {0: 'Toshkent', 1: 'Farg%60ona', 2: 'Farg%60ona', 3: 'Andijon', 4: 'Jizzax', 5: 'Samarqand', 6: 'Xiva',


# http://uzsmar    #         7: 'Buxoro', 8: 'Nukus', 9: 'Qarshi', 10: 'Navoiy', 11: 'Guliston', 12: 'Denov'}t.ru/namoz-vaqtlari/shahar/Andijon.html
# http://uzsmart.ru/namoz-vaqtlari/shahar/Jizzax.html
# http://uzsmart.ru/namoz-vaqtlari/shahar/Samarqand.html
# http://uzsmart.ru/namoz-vaqtlari/shahar/Xiva.html     xorazim
# http://uzsmart.ru/namoz-vaqtlari/shahar/Buxoro.html
# http://uzsmart.ru/namoz-vaqtlari/shahar/Nukus.html
# http://uzsmart.ru/namoz-vaqtlari/shahar/Qarshi.html   qashqar
# http://uzsmart.ru/namoz-vaqtlari/shahar/Navoiy.html
# http://uzsmart.ru/namoz-vaqtlari/shahar/Guliston.html     sirdaryo
# http://uzsmart.ru/namoz-vaqtlari/shahar/Denov.html    surxon

#
# print(quyosh)
# print(pewn)
# print(asr)
# print(shom)
# print(xufton)
