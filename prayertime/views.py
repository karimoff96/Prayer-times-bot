from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types
from .models import *
import telebot
from .prayer import pray_time
import requests
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

bot = telebot.TeleBot("5274232346:AAFL4UXhe41LbODSnp727iRhK4uCk3qonlI", parse_mode="HTML")


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
    if Users.objects.filter(user_id=message.from_user.id).exists():
        text = f'<i><b>Ассаламу алайкум ва рохматуллохи ва барокатух!\nАъ`узу билл`аҳи минаш-шайт`онир рож`ийм. Бисмилл`аҳир роҳм`анир роҳ`ийм</b></i>'
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        markup.add(btn, btn1)
        bot.send_message(message.from_user.id, text, reply_markup=markup)

    else:
        text = f'<b>Ассаламу алайкум {message.from_user.first_name}.</b>'
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        markup.add(btn, btn1)
        bot.send_message(message.from_user.id, text, reply_markup=markup)
        bot_user = Users.objects.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
        )
        bot_user.save()


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot_user = Users.objects.get(user_id=message.chat.id)
    if message.text in ["⌛Намоз вақтлари"]:
        bot_user.step = 1
        bot_user.save()
        markup = types.InlineKeyboardMarkup(row_width=2)
        b = types.InlineKeyboardButton('Тошкент', callback_data='tashkent')
        b1 = types.InlineKeyboardButton('Фарғона', callback_data='fergana')
        b2 = types.InlineKeyboardButton('Андижон', callback_data='andijan')
        b3 = types.InlineKeyboardButton('Наманган', callback_data='namangan')
        b4 = types.InlineKeyboardButton('Бухоро', callback_data='bukhara')
        b5 = types.InlineKeyboardButton('Жиззах', callback_data='jizzakh')
        b6 = types.InlineKeyboardButton('Қанши', callback_data='qarshi')
        b7 = types.InlineKeyboardButton('Нукус', callback_data='nukus')
        b9 = types.InlineKeyboardButton('Самарқанд', callback_data='samarkand')
        b10 = types.InlineKeyboardButton('Урганч', callback_data='urgench')
        b12 = types.InlineKeyboardButton('Хива', callback_data='khiva')
        b13 = types.InlineKeyboardButton('Гулистон', callback_data='gulistan')
        b15 = types.InlineKeyboardButton('Марғилон', callback_data='margilan')
        b11 = types.InlineKeyboardButton('Қўқон', callback_data='kokand')
        markup.add(b, b1, b2, b3, b4, b5, b6, b7, b9, b10, b11, b12, b13, b15)
        bot.send_message(message.from_user.id, "<u><b>🏘Ҳудудни танланг:</b></u>",
                         reply_markup=markup)
        markup1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn = types.KeyboardButton('🔙Ортга')
        markup1.add(btn)
        bot.send_message(message.from_user.id, "<i>Намоз вақтлари ҳудудларга қараб ўзгариши мумкин!</i>",
                         reply_markup=markup1)
    elif message.text == '🕋Намоз ўрганиш':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        b = types.KeyboardButton('👳‍♂Эркаклар учун')
        b1 = types.KeyboardButton('👳Аёллар учун')
        b2 = types.KeyboardButton('🔙Ортга')
        markup.add(b, b1, b2)
        bot.send_message(message.from_user.id,
                         f' <i><b>"Аҳлингизни намоз ( ўқиш ) га буюринг ва ( ўзингиз ҳам ) унга ( намозга ) бардошли бўлинг!” (Тоҳа, 132).</b></i>\nبِسْــــــــــــــــــــــمِ ﷲِالرَّحْمَنِ الرَّحِيم',
                         reply_markup=markup)
    elif message.text == '👳‍♂Эркаклар учун':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Бомдод намози ўқиш тартиби. \n👳‍♂ Еркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Видео дарс Пешин намозининг 4 ракат фарзи ўқиш тартиби. \nПешини намози суннатлари ҳам  шундай  ўқилади ниятда суннат дейилади 3-4 ракатда ҳам зам сура ўқилади. \n👳‍♂ Еркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Аср намози ўқиш тартиби. \n👳‍♂ Еркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Шом намози 3 ракат фарзи ўқиш тартиби. Шом намози икки ракат суннати овоз чиқармай ўқилади бомдодни икки ракат суннати каби фақат ният шомни икки ракат суннати деб қилинади. \n👳‍♂ Еркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Хуфтон намози 4 ракат фарзи ўқиш тартиби. \nХуфтон намози икки ракат суннати овоз чиқармай ўқилади бомдод суннати каби. \n👳‍♂ Еркаклар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345', caption='Тахаджуд намози.')
    elif message.text == '👳Аёллар учун':
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Аёллар учун Бомдод намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Аёллар учун Пешин намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Аёллар учун Аср намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345',
                       caption='Аёллар учун  Хуфтон намозини ўқиш тартиби. \n👳 Аёллар учун.')
        bot.send_video(chat_id=message.from_user.id, video='https://t.me/HDfixfilm/345', caption='Тахаджуд намози.')
    elif message.text == '🔙Ортга':
        markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btn = types.KeyboardButton("⌛Намоз вақтлари")
        btn1 = types.KeyboardButton("🕋Намоз ўрганиш")
        markup.add(btn, btn1)
        bot.send_message(message.from_user.id, '<b><i>Бисмилл`аҳир роҳм`анир роҳ`ийм</i></b>', reply_markup=markup)


# bot.polling()


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    if call.data in ['tashkent', 'fergana', 'andijan', 'namangan', 'bukhara', 'jizzakh', 'qarshi', 'nukus',
                     'navoiy', 'samarkand', 'urgench', 'termiz', 'khiva', 'gulistan', 'zarafshan', 'margilan',
                     'kokand']:
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        b2 = types.KeyboardButton('🔙Ортга')
        markup.add(b2)
        bot.send_message(call.from_user.id,
                         f'<i> "Аҳлингизни намоз ( ўқиш ) га буюринг ва ( ўзингиз ҳам ) унга ( намозга ) бардошли бўлинг!” (Тоҳа, 132)</i>.\nبِسْــــــــــــــــــــــمِ ﷲِالرَّحْمَنِ الرَّحِيم',
                         reply_markup=markup)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=pray_time(call.data))
