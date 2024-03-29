from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot import types
from .models import Send, User
from .prayer import pray_time, surahs
from environs import Env
from telebot.apihelper import ApiTelegramException
from django.http import HttpResponse

env = Env()
env.read_env()
bot = telebot.TeleBot(env.str('TOKEN'), parse_mode="HTML")
ADMINS = env.list('ADMINS')
CURRENT_ADMIN = None


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("<h1>Bot Url</h1>")
    elif request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


cities = {"27": 'Тошкент', '37': 'Фарғона', '1': 'Андижон', '15': 'Наманган',
          '4': "Бухоро", '9': 'Жиззах', '25': 'Қарши', '16': 'Нукус',
          '14': 'Навоий', '18': 'Самарқанд', '21': 'Хива', '5': 'Гулистон', '6': 'Денов',
          '26': 'Қўқон', '13': 'Марғилон', '3': 'Бишкек', '19': 'Туркистон',
          '61': 'Зарафшон', '20': 'Ўш', '78': 'Урганч', '74': 'Термиз', '39': 'Риштон'}

suras = ['Fotiha', 'Baqara', 'Imron', 'Niso', 'Maida', 'Anam', 'Arof', 'Anfol', 'Tavba', 'Yunus', 'Hud', 'Yusuf',
         'Rad', 'Ibrohim', 'Hijr', 'Nahl', 'Isro', 'Kahf', 'Maryam', 'Toha', 'Anbiyo', 'Haj', 'Muminun', 'Nur',
         'Furqon', 'Shuaro', 'Naml', 'Qasos', 'Ankabut', 'Rum', 'Luqmon', 'Sajda', 'Ahzob', 'Saba', 'Fotir', 'Yosin',
         'Soffat', 'Sod', 'Zumar', 'Gofir', 'Fussilat', 'Shoro', 'Zuxruf', 'Zuhan', 'Jathiya', 'Ahqaf', 'Muhammad',
         'Fath', 'Hujurat', 'Qof', 'Zuriyat', 'Tur', 'Najim', 'Qamar', 'Rohman', 'Voqiya', 'Hadid', 'Mujadila',
         'Hashir', 'Mumtahina', 'Soff', 'Juma', 'Munofiqun', 'Taghabun', 'Taloq', 'Tahrim', 'Mulk', 'Qalam', 'Haqqa',
         'Muorij', 'Nuh', 'jinn', 'Muzzammil', 'Muddathir', 'Qiyama', 'Insan', 'Mursalat', 'Naba', 'Naziat', 'Abasa',
         'Takawir', 'Infitar', 'Mutaffifeen', 'Inshiqaq', 'Burooj', 'Tariq', 'Ala', 'Ghashiya', 'Fajir', 'Balad',
         'Shams', 'Lail', 'Dhuha', 'Sharh', 'Teen', 'falaq', 'Qadr', 'Bayyina', 'Zilzila', 'Adiyat', 'Qaria',
         'Takathur', 'Asr', 'Hamza', 'Fil', 'Quraysh', 'Moun', 'Kavsar', 'Kofirun', 'Nosr', 'Masad', 'Ixlos', 'Falaq',
         'Nos']


@bot.message_handler(commands=["start"])
def start(message):
    if User.objects.filter(user_id=message.from_user.id).exists():
        bot_user = User.objects.get(user_id=message.chat.id)
        bot_user.active = True
        bot_user.step = 1
        bot_user.save()
        text = f'<i><b>Ассаламу алайкум ва рохматуллохи ва барокатух!\nАъ`узу билл`аҳи минаш-шайт`онир рож`ийм. Бисмилл`аҳир роҳм`анир роҳ`ийм</b></i>'
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(message.from_user.id, text, reply_markup=markup)

    else:
        text = f'<b>Ассаламу алайкум {message.from_user.first_name}.</b>'
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(message.from_user.id, text, reply_markup=markup)

        bot_user = User.objects.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            active=True,
            step=1
        )
        bot_user.save()
        for admin in ADMINS:
            bot.send_message(int(admin),
                             f'*Yangi foydalanuvchi * [{message.from_user.first_name}](tg://user?id={message.from_user.id})',
                             parse_mode='markdown')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot_user = User.objects.get(user_id=message.chat.id)

    if message.text in ["⌛Намоз вақтлари"]:
        bot_user.step = 1
        bot_user.save()
        markup = types.InlineKeyboardMarkup(row_width=2)
        b = types.InlineKeyboardButton('🕌Тошкент', callback_data='27')
        b1 = types.InlineKeyboardButton('🕌Фарғона', callback_data='37')
        b2 = types.InlineKeyboardButton('🕌Андижон', callback_data='1')
        b3 = types.InlineKeyboardButton('🕌Наманган', callback_data='15')
        b4 = types.InlineKeyboardButton('🕌Бухоро', callback_data='4')
        b5 = types.InlineKeyboardButton('🕌Жиззах', callback_data='9')
        b6 = types.InlineKeyboardButton('🕌Қарши', callback_data='25')
        b7 = types.InlineKeyboardButton('🕌Нукус', callback_data='16')
        b8 = types.InlineKeyboardButton('🕌Самарқанд', callback_data='18')
        b9 = types.InlineKeyboardButton('🕌Хива', callback_data='21')
        b10 = types.InlineKeyboardButton('🕌Гулистон', callback_data='5')
        b11 = types.InlineKeyboardButton('🕌Денов', callback_data='6')
        b12 = types.InlineKeyboardButton('🕌Навоий', callback_data='14')
        b13 = types.InlineKeyboardButton('🕌Қўқон', callback_data='26')
        b14 = types.InlineKeyboardButton('🕌Марғилон', callback_data='13')
        b15 = types.InlineKeyboardButton('🕌Бишкек', callback_data='3')
        b16 = types.InlineKeyboardButton('🕌Туркистон', callback_data='19')
        b17 = types.InlineKeyboardButton('🕌Зарафшон', callback_data='61')
        b18 = types.InlineKeyboardButton('🕌Ўш', callback_data='20')
        b19 = types.InlineKeyboardButton('🕌Урганч', callback_data='78')
        b20 = types.InlineKeyboardButton('🕌Термиз', callback_data='74')
        b22 = types.InlineKeyboardButton('🕌Риштон', callback_data='39')
        b21 = types.InlineKeyboardButton('🔙Ортга', callback_data='clear')

        markup.add(b, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b22, b14, b15, b16, b17, b20, b19, b18,
                   b21)
        bot.send_message(message.from_user.id, "<u><b>🏘Ҳудудни танланг:</b></u>", reply_markup=markup)

    elif message.text == '🕋Намоз ўрганиш':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        b = types.KeyboardButton('🚰Тахорат олиш')
        b0 = types.KeyboardButton('👳‍♂Эркаклар учун')
        b1 = types.KeyboardButton('👳Аёллар учун')
        b2 = types.KeyboardButton('🔙Ортга')
        markup.add(b)
        markup.add(b0, b1, b2)
        bot.send_message(message.from_user.id, 'بِسْــــــــــــــــــــــمِ ﷲِالرَّحْمَنِ الرَّحِيم')
        bot.send_message(message.from_user.id,
                         f' <i><b>"Аҳлингизни намоз ( ўқиш ) га буюринг ва ( ўзингиз ҳам ) унга ( намозга ) бардошли бўлинг!” (Тоҳа, 132).</b></i>',
                         reply_markup=markup)

    elif message.text == '🚰Тахорат олиш':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/128',
                       caption='Ният\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/129',
                       caption='Қўл\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/130',
                       caption='Оғиз\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/131',
                       caption='Бурун\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/135',
                       caption='Юз\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/134',
                       caption='Тирсак\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/133',
                       caption='Мустаҳаб\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/132',
                       caption='Оёқ\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')

    elif message.text == '👳‍♂Эркаклар учун':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12982',
                       caption='Бомдод намози ўқиш тартиби. \n👳‍♂ Эркаклар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12983',
                       caption='Видео дарс Пешин намозининг 4 ракат фарзи ўқиш тартиби. \nПешини намози суннатлари ҳам  шундай  ўқилади ниятда суннат дейилади 3-4 ракатда ҳам зам сура ўқилади. \n👳‍♂ Эркаклар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12984',
                       caption='Аср намози ўқиш тартиби. \n👳‍♂ Эркаклар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12985',
                       caption='Шом намози 3 ракат фарзи ўқиш тартиби. Шом намози икки ракат суннати овоз чиқармай ўқилади бомдодни икки ракат суннати каби фақат ният шомни икки ракат суннати деб қилинади. \n👳‍♂ Эркаклар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12986',
                       caption='Хуфтон намози 4 ракат фарзи ўқиш тартиби. \nХуфтон намози икки ракат суннати овоз чиқармай ўқилади бомдод суннати каби. \n👳‍♂ Эркаклар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12981',
                       caption='Тахаджуд намози.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')

    elif message.text == '👳Аёллар учун':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12976',
                       caption='Аёллар учун Бомдод намозини ўқиш тартиби. \n👳 Аёллар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12977',
                       caption='Аёллар учун Пешин намозини ўқиш тартиби. \n👳 Аёллар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12978',
                       caption='Аёллар учун Аср намозини ўқиш тартиби. \n👳 Аёллар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12979',
                       caption='Аёллар учун Шом намозини ўқиш тартиби. \n👳 Аёллар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12980',
                       caption='Аёллар учун  Хуфтон намозини ўқиш тартиби. \n👳 Аёллар учун.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12981',
                       caption='Тахаджуд намози.\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')

    elif message.text == '🔙Ортга':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '<b><i>Қуйидаги бўлимлардан бирини танланг:</i></b>',
                         reply_markup=markup)

    elif message.text == '📜Қуръон оятлари':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        b = types.KeyboardButton('🔙Ортга')
        markup.add(b)

        for i in range(1, len(suras) - 1, 3):
            markup.add(types.KeyboardButton(f"📖{suras[i - 1]}"), types.KeyboardButton(f"📖{suras[i]}"),
                       types.KeyboardButton(f"📖{suras[i + 1]}"))
        markup.add(b)
        bot.send_message(chat_id=message.from_user.id,
                         text="🌚Қуръон оятлари бўлими\n➖➖➖➖➖➖➖➖➖➖➖\nБарча суралар Мишари Рашид томонидан ижро этилган\n➖➖➖➖➖➖➖➖➖➖➖\nСурани танланг🌞\n➖➖➖➖➖➖➖➖➖➖➖",
                         reply_markup=markup)

    elif message.text[1:] in suras:
        bot.send_audio(chat_id=message.from_user.id, audio=surahs(message.text[1:])['id'],
                       caption=surahs(message.text[1:])['text'])

    elif message.text == '🔰Керакли дуолар':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        b = types.KeyboardButton('❇️Сано дуоси')
        b1 = types.KeyboardButton('❇️Аттахиёт дуоси')
        b2 = types.KeyboardButton('❇️Саловат')
        b3 = types.KeyboardButton('❇️Қунут дуоси')
        b4 = types.KeyboardButton('❇️Оятал курси')
        b5 = types.KeyboardButton('❇️Жаноза дуоси')
        b6 = types.KeyboardButton('🔙Ортга')
        markup.add(b, b1, b2, b3, b4, b5, b6)
        bot.send_message(message.from_user.id, "<u><b>✳️Дуони танланг:</b></u>", reply_markup=markup)

    elif message.text == '❇️Сано дуоси':
        bot.send_audio(chat_id=message.from_user.id, audio='https://t.me/masalalar_maruzalar/186',
                       caption='<b>Субҳанакаллоҳумма ва биҳамдика, ва табарокасмука, ва тааъла жаддука ва лаа илааҳа ғойрук.</b>\n\n<i>Маъноси: «Аллоҳим! Сенинг номинг муборакдир. Шон-шарафинг улуғдир. Сендан ўзга илоҳ йўқдир».</i>\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
    elif message.text == '❇️Аттахиёт дуоси':
        bot.send_audio(chat_id=message.from_user.id, audio='https://t.me/masalalar_maruzalar/189',
                       caption='<b>Аттаҳиййату лиллаҳи вассолавату ват­той­йибат.\nАссаламу ъалайка аййуҳан-набиййу ва роҳматуллоҳи вабарокатуҳ.\nАссаламу ъалайна ва аълаа ибаадиллааҳис солиҳийн.\nАшҳаду аллаа илааҳа иллаллоҳу ва ашҳаду анна Муҳаммадан ъабдуҳу ва росулуҳ</b>\n\n<i>Мазмуни: Мол, бадан, тил билан адо этиладиган бутун ибодатлар Аллоҳ учундир. Эй Набий! Аллоҳнинг раҳмати ва баракоти Сизга бўлсин. Сизга ва солиҳ қулларга Аллоҳнинг саломи бўлсин. Иқрорманки, Аллоҳдан ўзга илоҳ йўқ. Ва яна иқрорманки, Муҳаммад, алайҳиссалом, Аллоҳнинг қули ва элчисидирлар. </i>\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
    elif message.text == '❇️Саловат':
        bot.send_audio(chat_id=message.from_user.id, audio='https://t.me/masalalar_maruzalar/190',
                       caption='<b>Алл`оҳумма солли ъал`а Муҳаммадив-ва ъал`а `али Муҳаммад. Кам`а соллайта ъал`а Иброҳ`има ва ъал`а `али Иброҳ`им. Иннака ҳам`идум-маж`ид.\nАлл`оҳумма б`арик ъал`а Муҳаммадив-ва ъал`а `али Муҳаммад. Кам`а б`арокта ъал`а Иброҳ`има ва ъал`а `али Иброҳ`им. Иннака ҳам`идум-маж`ид.</b>\n\n<i>Мазмуни: Аллоҳим, Иброҳим ва унинг оиласига раҳмат этганинг каби, Муҳаммад ва ул зотнинг оиласига раҳмат айла, Сен ҳамду мақтовга лойиқ ва буюк Зотсан. \nАллоҳим, Иброҳим ва унинг оиласига баракотингни эҳсон этганинг каби Муҳаммад ва ул зотнинг оиласи устига ҳам баракотингни эҳсон айла. Сен ҳамду мақтовга лойиқ ва буюк Зотсан. </i>\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
    elif message.text == '❇️Қунут дуоси':
        bot.send_audio(chat_id=message.from_user.id, audio='https://t.me/masalalar_maruzalar/518',
                       caption='<b>Аллоҳумма! Иннаа настаъинука ва настағфирук.\nВа нуъмину бика ва натаваккалу ъалайка ва нусний ъалайкал хойр.\nНашкурука ва лаа накфурук. Ва нахлаъу ва натруку ман йафжурук.\nАллоҳумма! Иййаака наъбуду ва лака нусоллий ва насжуду, ва илайка насъаа ва наҳфиду, наржу роҳматака ва нахша ъазаабака, инна ъазаабака бил куффари мулҳиқ</b>\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
    elif message.text == '❇️Оятал курси':
        bot.send_audio(chat_id=message.from_user.id, audio='https://t.me/masalalar_maruzalar/211',
                       caption='<b>Аъ`узу билл`аҳи минаш-шайт`онир рож`ийм. Бисмилл`аҳир роҳм`анир роҳ`ийм. \nАлл`оҳу л`а ил`аҳа илл`а ҳувал ҳаййул қойй`ум. Л`а та’хузуҳ`у синатув-ва л`а на`вм. Лаҳу м`а фис-сам`ав`ати ва м`а фил арз. Манзаллаз`ий яшфаъу ъиндаҳ`у илл`а би’изниҳ. Яъламу м`а байна айд`иҳим ва м`а холфаҳум ва л`а йух`ит`уна би шай’им-мин ъилмиҳ`и илл`а бима ш`аъа. Васиъа курсиййуҳус-сам`ав`ати вал арз. Ва л`а йаъ`удуҳ`у ҳифзуҳум`а ва ҳувал ъаллиййул ъаз`ийм.</b>\n\n<i>Мазмуни: Аллоҳ — Ундан ўзга илоҳ йўқдир. (У ҳамиша) тирик ва абадий турувчидир. Уни на мудроқ тутар ва на уйқу. Осмонлар ва Ердаги (барча) нарсалар Уникидир. Унинг ҳузурида ҳеч ким (ҳеч кимни) Унинг рухсатисиз шафоат қилмас. (У) улар (одамлар)дан олдинги (бўлган) ва кейинги (бўладиган) нарсани билур. (Одамлар) Унинг илмидан фақат (У) истаганча ўзлаштирурлар. Унинг Курсийси осмонлар ва Ердан (ҳам) кенгдир. У иккисининг ҳифзи (тутиб туриши) Уни толиқтирмас. У олий ва буюкдир.</i>\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')
    elif message.text == '❇️Жаноза дуоси':
        bot.send_audio(chat_id=message.from_user.id, audio='https://t.me/masalalar_maruzalar/212',
                       caption='<b>Алл`оҳуммағфир лиҳаййин`а ва маййитин`а ва ш`аҳидин`а ва ғ`о’ибин`а ва соғ`ийрин`а ва каб`ийрин`а ва закарин`а ва унс`ан`а. Алл`оҳумма ман аҳйайтаҳ`у минн`а фааҳйиҳ`и ъалал Исл`ам. Ва ман таваффайту минн`а фатаваффаҳ`у ъалал ийм`ан.</b>\n\n<i>Маъноси: «Эй Раббим! Тиригимизни ва ўлигимизни, бу ерда бўлганларни ва бўлмаганларни, кичикларимизни ва катталаримизни, эркак ва аёлларимизни кечиргин. Аллоҳим, Биздан туғилажак янги наслларни Ислом динида дунёга келтир. Ажали етиб ҳаётдан кўз юмадиганларнинг жонларини имонли ҳолларида олгин». </i>\n\n<b>Яқинларингизга ҳам улашинг:</b>  <i>@namozvaqtlarirobot</i>')

    # ADMIN COMMANDS

    elif message.text == '/send' and str(message.chat.id) in ADMINS:
        CURRENT_ADMIN = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        b = types.KeyboardButton('🔙Ortga')
        markup.add(b)
        mesg = bot.send_message(CURRENT_ADMIN,
                                '<code>Blegilar soni 20 tadan kam bo`lmagan yozuvli habar yoki media kontent kiriting:</code>',
                                reply_markup=markup)
        bot.register_next_step_handler(mesg, send)

    elif message.text == "/stats":
        user = len(User.objects.all())
        bot.send_message(message.from_user.id,
                         f'🔰<b><i>БОТ СТАТИСТИКАСИ:</i></b>\n👥<b>Фойдаланувчилар сони:</b> {user}\n📖<b>Суралар сони:</b> {len(suras)}\n🧑🏻‍💻<b>Админ:</b><i> @dkarimoff96</i>')

    elif message.text == '/stop' and str(message.chat.id) in ADMINS:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        a = Send.objects.filter(id=1).first()
        bot.send_message(message.chat.id,
                         f'<b><i>Habar yuborish to`xtatildi.\nHozircha : {a.count} ta foydalanuvchiga yuborildi</i></b>',
                         reply_markup=markup)
        a.current = 0
        a.count = 0
        a.msg_id = 0
        a.save()

    else:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '<b><i>Қуйидаги бўлимлардан бирини танланг:</i></b>',
                         reply_markup=markup)


def send(elon):
    if elon.text == '🔙Ortga':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(elon.from_user.id, '<b><i>Қуйидаги бўлимлардан бирини танланг:</i></b>', reply_markup=markup)

    elif elon.content_type == 'text':
        senddd = Send.objects.get(id=1)
        if senddd.msg_id != 0:
            return bot.send_message(elon.from_user.id,
                             f"Hozir aktiv elon mavjud! uni (admin)[tg://user?id={senddd.admin_id} tomonidan yuborilyapti", parse_mode="markdown")
        elif len(elon.text) <= 20:
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn = types.KeyboardButton("⌛Намоз вақтлари")
            btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
            btn2 = types.KeyboardButton("🔰Керакли дуолар")
            btn3 = types.KeyboardButton("📜Қуръон оятлари")
            markup.add(btn, btn1, btn2, btn3)
            bot.send_message(elon.from_user.id,
                             '<b><i>Yuborilgan habar belgilar soni 20 tadan kam bo`lganligi sabali yuborilmadi!</i></b>',
                             reply_markup=markup)
            return bot.send_message(elon.from_user.id, '<b><i>Қуйидаги бўлимлардан бирини танланг:</i></b>',
                                    reply_markup=markup)

        users = User.objects.all()[:50]
        fail = 0
        success = 0
        for m in users:
            try:
                bot.copy_message(m.user_id, from_chat_id=elon.from_user.id, message_id=elon.id)
                success += 1
            except ApiTelegramException:
                fail += 1
        a = Send.objects.filter(id=1).first()
        a.current = 50
        a.count = success
        a.msg_id = elon.id
        a.save()
        bot.send_message(elon.from_user.id,
                         f'Habar foydalanuvchilarga yuborilmoqda...', )
    else:
        users = User.objects.all()[:50]
        fail = 0
        success = 0
        for m in users:
            try:
                bot.copy_message(m.user_id, from_chat_id=elon.from_user.id, message_id=elon.id)
                success += 1
            except ApiTelegramException:
                fail += 1
        a = Send.objects.filter(id=1).first()
        a.current = 50
        a.count = success
        a.msg_id = elon.id
        a.admin_id = elon.from_user.id
        a.save()
        bot.send_message(elon.from_user.id,
                         f'Habar foydalanuvchilarga yuborilmoqda...', )


def cronsend(request):
    msg = Send.objects.get(id=1)
    if msg.msg_id != 0:
        son = msg.current
        users = User.objects.all()[son:son + 50]

        if len(users) == 0:
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn = types.KeyboardButton("⌛Намоз вақтлари")
            btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
            btn2 = types.KeyboardButton("🔰Керакли дуолар")
            btn3 = types.KeyboardButton("📜Қуръон оятлари")
            markup.add(btn, btn1, btn2, btn3)
            us = len(User.objects.all())
            total = msg.count
            bot.send_message(int(ADMINS[0]),
                             f'<code><i>Jami foydalanuvchilar soni: {us}\nJo`natildi: {total}\nJo`natilmadi: {us - total}</i></code>',
                             reply_markup=markup)
            msg.current = 0
            msg.count = 0
            msg.msg_id = 0
            msg.save()
            response = HttpResponse()
            response.write("<h1>Habar yuborilishi muvofaqqiyatli yakunlandi!</h1>")
            return response
        fail = 0
        success = 0
        for m in users:
            try:
                bot.copy_message(m.user_id, from_chat_id=msg.admin_id, message_id=msg.msg_id)
                success += 1
            except ApiTelegramException:
                fail += 1
        a = Send.objects.filter(id=1).first()
        a.current = msg.current + 50
        a.count = msg.count + success
        a.save()
        response = HttpResponse()
        response.write("<h1>Habar yuborilmoqda!</h1>")
        return response
    response = HttpResponse()
    response.write("<h1>Habar yuborishda hatolik yuz berdi!</h1>")
    return response


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    if call.data in ['27', '37', '1', '15', '4', '9', '25', '16',
                     '18', '21', '5', '6', '14', '26', '13', '3', '19', '61', '20', '78', '74', '39']:

        bot_user = User.objects.get(user_id=call.from_user.id)
        bot_user.city = f'{cities[call.data]} - {call.data}'
        bot_user.save()
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("🔙Ортга", callback_data='back')
        item2 = types.InlineKeyboardButton("🔄Янгилаш", callback_data='refresh')
        markup.add(item2, item1)
        bot.edit_message_text(chat_id=call.from_user.id, text=pray_time(call.data), message_id=call.message.message_id,
                              reply_markup=markup)

    elif call.data == 'refresh':
        bot_user = User.objects.get(user_id=call.from_user.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("🔙Ортга", callback_data='back')
        item2 = types.InlineKeyboardButton("🔄Янгилаш", callback_data='refresh')
        markup.add(item2, item1)
        bot.delete_message(call.from_user.id, message_id=call.message.message_id)
        bot.send_message(call.from_user.id, text=pray_time(bot_user.city[-2:]), reply_markup=markup)
    elif call.data == 'clear':
        bot.delete_message(call.from_user.id, message_id=call.message.message_id)
        text = f'<i><b>Қуйидаги бўлимлардан бирини танланг:</b></i>'
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("🔰Керакли дуолар")
        btn3 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(call.from_user.id, text, reply_markup=markup)
    elif call.data == 'back':
        bot.delete_message(call.from_user.id, message_id=call.message.message_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        b = types.InlineKeyboardButton('🕌Тошкент', callback_data='27')
        b1 = types.InlineKeyboardButton('🕌Фарғона', callback_data='37')
        b2 = types.InlineKeyboardButton('🕌Андижон', callback_data='1')
        b3 = types.InlineKeyboardButton('🕌Наманган', callback_data='15')
        b4 = types.InlineKeyboardButton('🕌Бухоро', callback_data='4')
        b5 = types.InlineKeyboardButton('🕌Жиззах', callback_data='9')
        b6 = types.InlineKeyboardButton('🕌Қарши', callback_data='25')
        b7 = types.InlineKeyboardButton('🕌Нукус', callback_data='16')
        b8 = types.InlineKeyboardButton('🕌Самарқанд', callback_data='18')
        b9 = types.InlineKeyboardButton('🕌Хива', callback_data='21')
        b10 = types.InlineKeyboardButton('🕌Гулистон', callback_data='5')
        b11 = types.InlineKeyboardButton('🕌Денов', callback_data='6')
        b12 = types.InlineKeyboardButton('🕌Навоий', callback_data='14')
        b13 = types.InlineKeyboardButton('🕌Қўқон', callback_data='26')
        b14 = types.InlineKeyboardButton('🕌Марғилон', callback_data='13')
        b15 = types.InlineKeyboardButton('🕌Бишкек', callback_data='3')
        b16 = types.InlineKeyboardButton('🕌Туркистон', callback_data='19')
        b17 = types.InlineKeyboardButton('🕌Зарафшон', callback_data='61')
        b18 = types.InlineKeyboardButton('🕌Ўш', callback_data='20')
        b19 = types.InlineKeyboardButton('🕌Урганч', callback_data='78')
        b20 = types.InlineKeyboardButton('🕌Термиз', callback_data='74')
        b22 = types.InlineKeyboardButton('🕌Риштон', callback_data='39')
        b21 = types.InlineKeyboardButton('🔙Ортга', callback_data='clear')
        markup.add(b, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b22, b14, b15, b16, b17, b20, b19, b18,
                   b21)
        bot.send_message(call.from_user.id, "<u><b>🏘Ҳудудни танланг:</b></u>", reply_markup=markup)
