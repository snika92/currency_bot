import telebot
import os
from telebot import types
from utils.utils import get_currency_rate
from utils.utils import save_to_json
import time
import json

API_KEY = os.getenv("C_bot")
bot = telebot.TeleBot(API_KEY)
CURRENCY_RATES_FILE = os.path.join("..", "src", "currency_rates.json")


def compare_to_previous_rate(currency, from_):
    rate = get_currency_rate(currency)
    with open(CURRENCY_RATES_FILE) as json_file:
        data_list = json.load(json_file)
    for array in data_list[::-1]:
        if currency == array['Currency']:
            if rate != array['Rate']:
                bot.send_message(from_, f'Курс {currency} к рублю изменился: {rate}', time.sleep(5))
            else:
                bot.send_message(from_, f'Курс не изменился: {rate}', time.sleep(5))
        break


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Могу помочь узнать курс USD или EUR", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text in ['👋 Поздороваться', 'Нет, спасибо']:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('USD')
        btn2 = types.KeyboardButton('EUR')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Выберите валюту', reply_markup=markup)  # ответ бота
    elif message.text in ['USD', 'EUR']:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Подписаться')
        btn2 = types.KeyboardButton('Нет, спасибо')
        markup.add(btn1, btn2)
        rate = get_currency_rate(message.text)
        bot.send_message(message.from_user.id, f'Курс {message.text} к рублю: {rate}', parse_mode='Markdown')
        bot.send_message(message.from_user.id, f'Хотите подписаться на изменения?', parse_mode='Markdown', reply_markup=markup)
        save_to_json(message.text, rate)
    elif message.text == 'Подписаться':
        user_id = message.chat.id
        compare_to_previous_rate('USD', user_id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('USD')
        btn2 = types.KeyboardButton('EUR')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Выберите валюту', reply_markup=markup)  # ответ бота
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Здесь вы можете узнать курс USD или EUR")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
