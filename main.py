import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Добрый день, {message.chat.username}")
    text = 'Чтобы начать работу с ботом, введите команду в формате: \n<Наименование валюты>|\
<в какую валюту производится перевод>|\
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        quote, base, amount = value

        if len(value) != 3:
            raise ConvertionException('Слишком много параметров.')
        res = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} - {res} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()

