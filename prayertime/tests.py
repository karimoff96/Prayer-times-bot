from django.test import TestCase

import requests
from bs4 import BeautifulSoup

url = 'https://islom.uz/vaqtlar/13/2'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
city = soup.find_all('span', class_='p_menu')[11:24]
time = soup.find_all('td', class_='sahar bugun')
# for c in city:
#     print(c.text)
print(time)



