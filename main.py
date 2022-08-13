import asyncio
import telebot.async_telebot
import config
import message as msg_text
from telebot import types


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def basic_commands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='О нас'))
    markup.add(types.KeyboardButton(text='Услуги'))
    markup.add(types.KeyboardButton(text='Поддержка'))
    text = msg_text.RegularUser().start()
    await bot.send_message(message.chat.id, text, reply_markup=markup)


async def services(message):
    text = msg_text.RegularUser().services()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Разработка чат-ботов', callback_data='develop_bots'))
    markup.add(types.InlineKeyboardButton(text='Реклама у блогеров', callback_data='bloggers'))
    markup.add(types.InlineKeyboardButton(text='Продвижение в телеграмм', callback_data='telegram'))
    markup.add(types.InlineKeyboardButton(text='Создание сайтов', callback_data='sites'))
    markup.add(types.InlineKeyboardButton(text='Дизайн', callback_data='design'))
    await bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'develop_bots')
async def develop_bots(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'bloggers')
async def bloggers(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'telegram')
async def telegram(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'sites')
async def sites(callback):
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'design')
async def design(callback):
    ...


@bot.message_handler(content_types=['text'])
async def echo(message):

    await bot.send_message(message.chat.id, message.text)





async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())