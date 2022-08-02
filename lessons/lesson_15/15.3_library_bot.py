import telebot
from telebot import apihelper
import time

#Прокси сервера
# https://hidemy.name/ru/proxy-list/?country=FR&type=hs#list

TOKEN = '5449407787:AAHs7AbrX9ygAab41TfoTRJ0Hp8c0uY1SdU'

proxies = {
    'http': 'http://173.245.49.25:80',
}

apihelper.proxy = proxies
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def command_start(message):
    bot.reply_to(message, 'Рад Вас приветствовать')

@bot.message_handler(commands = ['admin'], func = lambda message: message.from_user.id == 490490869)
def admin(message):
    print(message)
    bot.reply_to(message,'Приветствую, Хозяин')

@bot.message_handler(commands = ['admin_'])
def admin(message):
    if message.from_user.id == 490490869:
        bot.reply_to(message,'Приветствую, Хозяин')
    else:
        bot.reply_to(message,'Ты не мой Хозяин')
#
# @bot.message_handler(content_types = ['text'])
# def text_t(message):
#     text = message.text
#     bot.reply_to(message, f'Вы сказали:{text}')
#     # bot.reply_to(message, text[::-1])

@bot.message_handler(content_types = ['text'])
def text_t(message):
    text = message.text
    if text == 'как дела' or text == 'как ты':
        bot.reply_to(message, "У меня все хорошо. А у тебя как?")
    elif text == 'У меня тоже все хорошо' or text == 'У меня супер!':
        bot.reply_to(message, "Рад за тебя. Чем можешь порадовать?")
    elif text == 'Я учу питон' or text == 'Есть продвижения в питоне':
        bot.reply_to(message, "Ты молодец")




# # комманда админ
# @bot.message_handler(commands = ['admin'])
# def admin(message):
#     # if (message.from_user.username == 'tahoe_ivanova'):
#         bot.reply_to(message, 'Салют, Натали!')
# комманда help
# @bot.message_handler(commands = ['help'])
# def help_me(message):
#     bot.reply_to(message, 'Мне нечем тебе помочь...')
#
# @bot.message_handler(commands=['hello'])
# #@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == SOME_FANCY_EMOJI)
# def send_something(message):
#     bot.reply_to(message, 'Очень мило.')

bot.polling()