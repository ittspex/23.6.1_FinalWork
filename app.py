import telebot
from config import keys
from extensions import ConvertionException, CurrencyConverter

TOKEN = '7175161775:AAHx3tlYVJ4aRmmKZ5vui3M7wFUJzoFXxK4'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start',])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате: \n<Имя валюты> \
    <В какую валюту перевести> \
    <Количество переводимой валюты> \n <Увидеть список всех доступных валют введя команду: /values \n - Нужна помощь нажми , команду /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help',])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате: \n<Имя валюты> \
    <В какую валюту перевести> \
    <Количество переводимой валюты> \n <Увидеть список всех доступных валют введя команду: /values \n - Хочешь начать работу нажми команду /start'
    bot.reply_to(message, text)
@bot.message_handler(commands=['values',])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()