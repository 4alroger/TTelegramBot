import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN) # создаем бот с параметром TOKEN


@bot.message_handler(commands=['start', 'help']) # функция ответа бота на команды /start и /help
def start(message: telebot.types.Message):
    text = 'Здравствуйте! Чтобы начать работу, введите команду в следующем формате: \n ' \
           '\
<наименование валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Список доступных к конвертации валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values']) # функция ответа бота на команду /values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3: # если код валюты не равен 3 знакам, то выводим соответствующее сообщение
            raise APIException('Неверное количество параметров!')
        answer = Convertor.get_price(*values)
    except APIException as e: # если отрабатывается ощибка в коде, выводим сообщение
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e: # все остальные ошибки
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(non_stop=True)