"""
Бот для астро-канала Екатерины
"""

import telebot
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
path = 'D:/PYTHON/Programms/bot_config/inputKate/'
API_KEY = read_id_or_api_key(path + 'API_KEY')
TEACHER_ID = int(read_id_or_api_key(path + 'teacher_id'))

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands = ['start'])
def welcome(message):
    #Метод работает, когда запускаем бота в первый раз (/start)
    bot.send_message(message.chat.id, "Приветствую, {0.first_name}!\n"
                                      "В этот бот вы можете отправить любое сообщение, оно будет анонимным."
                                      .format(message.from_user),
                     parse_mode='html' #разметка html
                     )

@bot.message_handler(content_types = ['text'])
def lalala(message):
    if message.chat.type == 'private':
        if len(message.text) > 500:
            bot.reply_to(message,
                         'Прости, сообщение слишком большое. Попробуй разбить вопрос на части и попробовать ещё раз.')
            return

        answer = f"""Благодарю, {message.from_user.first_name}! В ближайшее время вы получите ответ."""

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

