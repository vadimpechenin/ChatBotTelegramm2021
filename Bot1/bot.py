"""
Test code of bot to Telegram from https://www.youtube.com/watch?v=M8fhrtvedHA&t=620s
https://core.telegram.org/bots/api - документация

https://github.com/limepillX/anon_questions_bot?ysclid=m7eb1wox8s530914684

Test5MasaBot
"""
#pip install pyTelegramBotAPI - v 4.1.0
#config - import config.py
import telebot
import config
import json
import datetime as dt

#Библиотеки для работы с клавиатурой
import random
from telebot import types


def read_id_or_api_key(file_path):
    with open(file_path, 'r+') as f:
        key = f.readline().strip()
        assert key
        print(f'Got {file_path.split("/")[-1]}')
    return key



#bot = telebot.TeleBot(config.TOKEN)
path = 'D:/PYTHON/Programms/bot_config/input/'
API_KEY = read_id_or_api_key(path + 'API_KEY')
TEACHER_ID = int(read_id_or_api_key(path + 'teacher_id'))

bot = telebot.TeleBot(API_KEY)

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
            if len(message.text) > 500:
                bot.reply_to(message,
                             'Прости, сообщение слишком большое. Попробуй разбить вопрос на части и попробовать ещё раз.')
                return

            answer = f"""Хорошо, твой вопрос: "{message.text}"
            Успешно записан. На следующей лекции постараюсь разобрать.🙃"""

            print(f'\nGot new question: "{message.text}"')

            bot.send_message(chat_id=TEACHER_ID, text=f'❗Новый вопрос, "{message.text}"')

            try:
                message.text.encode(encoding='utf-8')
            except UnicodeEncodeError:
                print('Сообщение не записано из-за проблем с кодировкой.')
                bot.reply_to(message, 'Произошла ошибка, попробуй удалить спец. символы и смайлики')
                return

            try:
                file_data['number_of_questions'] += 1
            except:
                file_data['number_of_questions'] = 1

            file_data[str(file_data['number_of_questions'])] = {
                'date': str(dt.datetime.now().date()),
                'time': str(dt.datetime.now().time())[:-10],
                'text': message.text
            }

            write_to_file(file_data)
            bot.reply_to(message, answer)

            #bot.send_message(message.chat.id, 'Я не знаю что ответить ☝, ваш запрос отослан человеку')

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


def read_file():
    with open('output/questions.json', 'r', encoding='utf-8') as f:
        try:
            data = json.loads(f.read())
            print('Content loaded from json')
        except json.JSONDecodeError:
            print('Questions file is empty, filling...')
            write_to_file({"number_of_questions": 0})
            data = read_file()

    return data

def write_to_file(data):
    with open('output/questions.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
        print(f'Content written in json\n')


if __name__ == '__main__':
    file_data = read_file()
    #BOT.infinity_polling(timeout=5)
    #RUN
    bot.polling(none_stop=True)

