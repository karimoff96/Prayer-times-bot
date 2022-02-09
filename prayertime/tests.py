from datetime import timezone, datetime, timedelta
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'http://uzsmart.ru/namoz-vaqtlari/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

current_time = soup.find('span', id='current_time').text  # current time tayyor

quotes = soup.find('table', style='font-size: 24px')
part = quotes.find_all('tr', class_='item')
tong = part[0].text[14:]  # tong/sahar +
quyosh = part[1].text[8:]
pewn = part[2].text[8:]
asr = part[3].text[5:]
shom = part[4].text[14:]
xufton = part[5].text[8:]



