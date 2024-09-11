import telebot
from config import currencies, TOKEN
from extensions import APIException, СurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Добро пожаловать! Хотите узнать обменный курс? Для начала работы введите команду в следующем формате:\n \
<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nОтобразить список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for currency in currencies.keys():
        text = "\n".join((text, currency))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
        values = message.text.split(" ")

        if len(values) > 3:
            raise APIException("Указано слишком много параметров.")
    
        base, quote, amount = values
        total_base = СurrencyConverter.get_price(base, quote, amount)
    
        text = f"Цена {amount} {base} в {quote} = {total_base}"
        bot.send_message(message.chat.id, text)
    

bot.polling()
