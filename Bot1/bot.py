"""
Test code of bot to Telegram from https://www.youtube.com/watch?v=M8fhrtvedHA&t=620s
Test5MasaBot
"""
#pip install pyTelegramBotAPI - v 4.1.0
#config - import config.py
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types = ['text'])
def lalala(message):
    bot.send_message(message.chat.id, message.text)

#RUN
bot.polling(none_stop=True)

