import asyncio
import telebot.async_telebot
import config


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


@bot.message_handler(content_types=['text'])
async def echo(message):
    await bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['start', 'help'])
async def basic_commands(message):
    await bot.send_message(message.chat.id, 'Hello world!')


async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())