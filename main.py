import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Здравствуйте! Введите /help для просмотра доступных команд."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = "Доступные команды: /start (начало работы с ботом), /values (список валют для конвертации), /help (доступные команды), /convert (запуск конвертации)"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберите валюту, из которой конвертировать'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберите валюту, в которую конвертировать, (вводить валюту в формате списка доступных валют)'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Выберите количество конвертируемой валюты'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Convertor.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n {e}")
    else:
        text = new_price
        bot.send_message(message.chat.id, text)




@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    val = message.text.split()
    try:
        if len(val) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*val)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling()