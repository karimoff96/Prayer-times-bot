from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot import types
from .models import *
from .prayer import pray_time
from environs import Env
import json

env = Env()
env.read_env()
bot = telebot.TeleBot(env.str('TOKEN'), parse_mode="HTML")
Admin = env.int('ADMIN')


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


@bot.message_handler(commands=["start"])
def start(message):
    if User.objects.filter(user_id=message.from_user.id).exists():
        bot_user = User.objects.get(user_id=message.chat.id)
        bot_user.active = True
        bot_user.step = 1
        bot_user.save()
        text = f'<i><b>Ассаламу алайкум ва рохматуллохи ва барокатух!\nАъ`узу билл`аҳи минаш-шайт`онир рож`ийм. Бисмилл`аҳир роҳм`анир роҳ`ийм</b></i>'
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1)
        markup.add(btn2)
        bot.send_message(message.from_user.id, text, reply_markup=markup)

    else:
        text = f'<b>Ассаламу алайкум {message.from_user.first_name}.</b>'
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1)
        markup.add(btn2)
        bot.send_message(message.from_user.id, text, reply_markup=markup)

        if message.from_user.username != None:
            bot.send_message(Admin, f'<b>Yangi foydalanuvchi <i>@{message.from_user.username}</i></b>')
        else:
            bot.send_message(Admin, f'<b>Yangi foydalanuvchi <i>{message.from_user.id}</i></b>')
        bot_user = User.objects.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            active=True,
            step=1
        )
        bot_user.save()


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
        b16 = types.InlineKeyboardButton('🕌Туркмстон', callback_data='19')
        b17 = types.InlineKeyboardButton('🕌Зарафшон', callback_data='61')
        b18 = types.InlineKeyboardButton('🕌Ўш', callback_data='20')
        b19 = types.InlineKeyboardButton('🕌Урганч', callback_data='78')
        b20 = types.InlineKeyboardButton('🕌Термиз', callback_data='74')
        markup.add(b, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20)
        bot.send_message(message.from_user.id, "<u><b>🏘Ҳудудни танланг:</b></u>", reply_markup=markup)

    elif message.text == '🕋Намоз ўрганиш':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        b = types.KeyboardButton('💦Тахотар')
        b0 = types.KeyboardButton('👳‍♂Эркаклар учун')
        b1 = types.KeyboardButton('👳Аёллар учун')
        b2 = types.KeyboardButton('🔙Ортга')
        markup.add(b)
        markup.add(b0, b1, b2)
        bot.send_message(message.from_user.id, 'بِسْــــــــــــــــــــــمِ ﷲِالرَّحْمَنِ الرَّحِيم')
        bot.send_message(message.from_user.id,
                         f' <i><b>"Аҳлингизни намоз ( ўқиш ) га буюринг ва ( ўзингиз ҳам ) унга ( намозга ) бардошли бўлинг!” (Тоҳа, 132).</b></i>',
                         reply_markup=markup)

    elif message.text == '💦Тахотар':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/128', caption='Ният')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/129', caption='Қўл')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/130', caption='Оғиз')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/131', caption='Бурун')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/135', caption='Юз')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/134', caption='Тирсак')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/133', caption='Мустаҳаб')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/quran_u/132', caption='Оёқ')

    elif message.text == '👳‍♂Эркаклар учун':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12982',
                       caption='Бомдод намози ўқиш тартиби. \n👳‍♂ Эркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12983',
                       caption='Видео дарс Пешин намозининг 4 ракат фарзи ўқиш тартиби. \nПешини намози суннатлари ҳам  шундай  ўқилади ниятда суннат дейилади 3-4 ракатда ҳам зам сура ўқилади. \n👳‍♂ Эркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12984',
                       caption='Аср намози ўқиш тартиби. \n👳‍♂ Эркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12985',
                       caption='Шом намози 3 ракат фарзи ўқиш тартиби. Шом намози икки ракат суннати овоз чиқармай ўқилади бомдодни икки ракат суннати каби фақат ният шомни икки ракат суннати деб қилинади. \n👳‍♂ Эркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12986',
                       caption='Хуфтон намози 4 ракат фарзи ўқиш тартиби. \nХуфтон намози икки ракат суннати овоз чиқармай ўқилади бомдод суннати каби. \n👳‍♂ Эркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12981',
                       caption='Тахаджуд намози.')

    elif message.text == '👳Аёллар учун':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12976',
                       caption='Аёллар учун Бомдод намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12977',
                       caption='Аёллар учун Пешин намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12978',
                       caption='Аёллар учун Аср намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12979',
                       caption='Аёллар учун Шом намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12980',
                       caption='Аёллар учун  Хуфтон намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/ishonchlihadislar/12981',
                       caption='Тахаджуд намози.')

    elif message.text == '🔙Ортга':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1)
        markup.add(btn2)
        bot.send_message(message.from_user.id, '<b><i>Бисмилл`аҳир роҳм`анир роҳ`ийм</i></b>', reply_markup=markup)
    elif message.text == '📜Қуръон оятлари':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        b = types.KeyboardButton('🔙Ортга')
        markup.add(b)
        with open('./data.json', 'r') as file:
            data = json.load(file)
            for i in range(1, len(data) - 1, 3):
                markup.add(types.KeyboardButton(data[i - 1]['sura']), types.KeyboardButton(data[i]['sura']),
                           types.KeyboardButton(data[i + 1]['sura']))
        markup.add(b)
        bot.send_message(chat_id=message.from_user.id,
                         text="🌚Қуръон оятлари бўлими\n➖➖➖➖➖➖➖➖➖➖➖\nБарча суралар Мишари Рашид томонидан ижро этилган\n➖➖➖➖➖➖➖➖➖➖➖\nСурани танланг🌞\n➖➖➖➖➖➖➖➖➖➖➖",
                         reply_markup=markup)

    elif message.text == '/send' and message.chat.id == Admin:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        b = types.KeyboardButton('🔙Ortga')
        markup.add(b)
        mesg = bot.send_message(Admin, '<code>Elonni kiriting:</code>', reply_markup=markup)
        bot.register_next_step_handler(mesg, send)

    elif message.text == '/activate' and message.chat.id == Admin:
        for i in User.objects.all():
            i.active = True
            i.step = 1
            i.save()
        bot.send_message(Admin,
                         "<code>Barcha foydalanuvchilar holati aktivlashtirildi!\nAdmin tomonidan yubordilgan habarlar barcha foydalanuvchilarga ham jo`natiladi</code>")

    elif message.text == '/deactivate' and message.chat.id == Admin:
        for i in User.objects.all():
            if i.user_id != Admin:
                i.active = False
                i.step = 0
                i.save()
        bot.send_message(Admin,
                         "<code>Barcha foydalanuvchilar holati muzlatildi!\nAdmin tomonidan yuborilgan elonlar boshqa foydlanuvchilarga yuborilmaydi</code>")

    elif message.text == "/stats" and message.chat.id == Admin:
        user = len(User.objects.all())
        bot.send_message(Admin,
                         f'🔰<b><i>Bot statistikasi:</i></b>\n👥<b>Foydalanuvchilar:</b> {user}\n🧑🏻‍💻<b>Muallif:</b><i> @dkarimoff96</i>')

    elif message.text == '🔙Ortga':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1)
        markup.add(btn2)
        bot.send_message(message.from_user.id, '<b><i>Бисмилл`аҳир роҳм`анир роҳ`ийм</i></b>', reply_markup=markup)


def send(elon):
    if elon.text == '🔙Ortga':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1)
        markup.add(btn2)
        bot.send_message(elon.from_user.id, '<b><i>Бисмилл`аҳир роҳм`анир роҳ`ийм</i></b>', reply_markup=markup)

    else:
        for m in User.objects.all():
            bot.copy_message(chat_id=m.user_id, from_chat_id=elon.chat.id, message_id=elon.id)
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        btn2 = types.KeyboardButton("📜Қуръон оятлари")
        markup.add(btn, btn1)
        markup.add(btn2)
        bot.send_message(elon.from_user.id, '<code><i>E`lon foydalanuvchilarga muvaffaqiyatli jo`natildi</i></code>',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    if call.data in ['27', '37', '1', '15', '4', '9', '25', '16',
                     '18', '21', '5', '6', '14', '26', '13', '3', '19', '61', '20', '78', '74']:
        bot_user = User.objects.get(user_id=call.from_user.id)
        bot_user.address = call.data
        bot_user.step = 3
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
        bot.send_message(call.from_user.id, text=pray_time(bot_user.address), reply_markup=markup)

    elif call.data == 'back':
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
        b16 = types.InlineKeyboardButton('🕌Туркмстон', callback_data='19')
        b17 = types.InlineKeyboardButton('🕌Зарафшон', callback_data='61')
        b18 = types.InlineKeyboardButton('🕌Ўш', callback_data='20')
        b19 = types.InlineKeyboardButton('🕌Урганч', callback_data='78')
        b20 = types.InlineKeyboardButton('🕌Термиз', callback_data='74')
        markup.add(b, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20)
        bot.send_message(call.from_user.id, "<u><b>🏘Ҳудудни танланг:</b></u>", reply_markup=markup)
