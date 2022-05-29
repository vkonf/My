
import telebot
from init import keys, Token
from api_maker import CryptoConverter, ConvertionException




bot = telebot.TeleBot(Token)




# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text='Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты> \n' \
         'пример: солана рубль 1\nувидеть список всех доступных валют /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text='Доступные команды:\n/values - доступные валюты\n'
    bot.reply_to(message,text)

# Обрабатываются все сообщения, содержащие команды '/values'.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text,key,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertionException('Неправильное количество параметров')
        quote, base, amount = values
        total_base=CryptoConverter.convert(quote,base,amount)
    except ConvertionException as b:
        bot.reply_to(message, f'Ошибка пользователя\n{b}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)





bot.polling(none_stop=True)


# Обрабатывается все документы и аудиозаписи
#@bot.message_handler(content_types=['document', 'audio'])
#def handle_docs_audio(message):
#    pass



