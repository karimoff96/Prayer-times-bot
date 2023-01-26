import json

x = '''Fotiha
Baqara
Imron
Niso
Maida
Anam
Arof
Anfol
Tavba
Yunus
Hud
Yusuf
Rad
Ibrohim
Hijr
Nahl
Isro
Kahf
Maryam
Toha
Anbiyo
Haj
Muminun
Nur
Furqon
Shuaro
Naml
Qasos
Ankabut
Rum
Luqmon
Sajda
Ahzob
Saba
Fotir
Yosin
Soffat
Sod
Zumar
Gofir
Fussilat
Shoro
Zuxruf
Zuhan
Jathiya
Ahqaf
Muhammad
Fath
Hujurat
Qof
Zuriyat
Tur
Najim
Qamar
Rohman
Voqiya
Hadid
Mujadila
Hashir
Mumtahina
Soff
Juma
Munofiqun
Taghabun
Taloq
Tahrim
Mulk
Qalam
Haqqa
Muorij
Nuh
jinn
Muzzammil
Muddathir
Qiyama
Insan
Mursalat
Naba
Naziat
Abasa
Takawir
Infitar
Mutaffifeen
Inshiqaq
Burooj
Tariq
Ala
Ghashiya
Fajir
Balad
Shams
Lail
Dhuha
Sharh
Teen
falaq
Qadr
Bayyina
Zilzila
Adiyat
Qaria
Takathur
Asr
Hamza
Fil
Quraysh
Moun
Kavsar
Kofirun
Nosr
Masad
Ixlos
Falaq
Nos'''
import json

x = x.split()
data = {}
for i in range(len(x)):
    data[f'{x[i]}'] = {'id': f'https://t.me/quran_u/{i + 3}', 'text': f'{x[i]} surasi'}
    with open('../data.json', 'w') as file:
        file.write(json.dumps(data))

    # with open('../data.json', 'r') as file:
    #     data = json.load(file)
    #
    # for i in range(len(data)):
    #     print(data[i]['sura'])
