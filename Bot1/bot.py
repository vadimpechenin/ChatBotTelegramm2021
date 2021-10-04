"""
Test code of bot to Telegram from https://www.youtube.com/watch?v=M8fhrtvedHA&t=620s
https://core.telegram.org/bots/api - документация

Test5MasaBot
"""
#pip install pyTelegramBotAPI - v 4.1.0
#config - import config.py
import telebot
import config

#Библиотеки для работы с клавиатурой
import random
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ['start'])
def welcome(message):
    #Метод работает, когда запускаем бота в первый раз (/start)
    sti = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #keyboard
    #Создание обычной клавиатуры и прикрепление к сообщению. resize_keyboard - маленькая клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    #Кнопки клавиатуры
    item1 = types.KeyboardButton("4️⃣ Рандомное число")
    item2 = types.KeyboardButton("👋 Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот созданный чтобы быть подопытным кроликом.".format(message.from_user,
                                                                                             bot.get_me()),
                     parse_mode='html', #разметка html
                     reply_markup=markup #прикрепить клавиатуру
                     )



@bot.message_handler(content_types = ['text'])
def lalala(message):
    #Реализация эхо-бота
    #bot.send_message(message.chat.id, message.text)
    #Адекватные ответы
    if message.chat.type == 'private':
        if message.text == '4️⃣ Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == '👋 Как дела?':

            #Второй тип клавиатуры (инлайновая)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить ☝️')

#Обработка нажатия на кнопку инлайновой клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает и хуже')

            #remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="👋 Как дела?", reply_markup=None)

            #Уведомление
            bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text = "Это тестовое уведомление")

    except Exception as e:
        print(repr(e))
#RUN
bot.polling(none_stop=True)

