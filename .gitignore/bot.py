# -*- coding: utf-8 -*-

import pyowm
import telebot
from datetime import datetime, timedelta

# from telebot import apihelper
# apihelper.proxy = {'https': 'socks5://telegram.vpn99.net:55655'}

owm = pyowm.OWM('5d952a0a731f297a28ac1be1c9a2c6d7', language = 'ru')

bot = telebot.TeleBot('1195784483:AAH3fHJym1RDxTsFoUrWS2NK3C7i7rPqhr4')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Введи город, чтобы получить температуру.")

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio', 'sticker', 'photo', 'video', 'video_note', 'voice', 'location', 'contact'])
def handle_docs_audio(message):
	pass

@bot.message_handler(content_types=['text'])
def send_echo(message):
  try:
    if(not owm.is_API_online):
      bot.send_message(message.chat.id, 'API офлайн, погоди немножко.')
    else:
      observation = owm.weather_at_place(message.text)
      w = observation.get_weather()
      temp = w.get_temperature('celsius')['temp']
      rain = w.get_rain()
      wind = w.get_wind()
      
      answer = f"В славном городе {message.text} сейчас {w.get_detailed_status()}. \n"
      answer += f"Температура около {round(temp)} градусов.\n\n"

      if temp < 10:
        answer += 'Холодно, одевайся получше.\n\n'
      elif temp < 17:
        answer += 'Прохладно, лучше что-нибудь накинуть сверху.\n\n'
      else:
        answer += 'Не холодно, можно в футболке щеголять.\n\n'
    

      bot.send_message(message.chat.id, answer)
    
  except pyowm.exceptions.api_response_error.NotFoundError:
      bot.send_message(message.chat.id, 'Твой город не найден. Введи полное название города, чтобы я показал тебе температуру.')
      

bot.polling(none_stop = True)
