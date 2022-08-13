import asyncio
import telebot.async_telebot
import config
import message as msg_text
from telebot import types
import models

bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def basic_commands(message):
    models.db_object.db_insert(bot, message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='О нас'))
    markup.add(types.KeyboardButton(text='Услуги'))
    markup.add(types.KeyboardButton(text='Поддержка'))
    text = msg_text.RegularUser().start()
    await bot.send_message(message.chat.id, text, reply_markup=markup)
    await services(message)


@bot.message_handler(commands=['admin'])
async def administration(message):
    ...


async def services(message):
    text = msg_text.Basement().services()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Разработка чат-ботов', callback_data='develop_bots'))
    markup.add(types.InlineKeyboardButton(text='Реклама у блогеров', callback_data='bloggers'))
    markup.add(types.InlineKeyboardButton(text='Продвижение в телеграмм', callback_data='promotion_telegram'))
    markup.add(types.InlineKeyboardButton(text='Создание сайтов', callback_data='sites'))
    markup.add(types.InlineKeyboardButton(text='Дизайн', callback_data='design'))
    await bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'develop_bots')
async def develop_bots(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'bloggers')
async def bloggers(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'promotion_telegram')
async def telegram(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'sites')
async def sites(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'design')
async def design(callback):
    ...


@bot.message_handler(content_types=['text'])
async def get_messages(message):
    if message.text == 'О нас':
        text = msg_text.Basement().about()
        await bot.send_message(message.chat.id, text)
    elif message.text == 'Услуги':
        await services(message)
    elif message.text == 'Поддержка':
        text = msg_text.Basement().support()





async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())