import asyncio
import telebot.async_telebot
import config
import message as msg_text
from telebot import types
import models


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


def clear_flags(message, callback=False, not_delete=()):
    if callback:
        message = message.message
    flags = (
             'msg_text.dev_bots.flag_develop_bots', 'msg_text.prom_tg.flag_prom_tg',
             'msg_text.prom_tg.category', 'msg_text.base.flag_support',
             'msg_text.site.flag_sites',
             'msg_text.design_obj.flag_design',
             'msg_text.site.flag_sup_brief',
             'msg_text.design_obj.flag_sup_brief'
             )
    for flag in flags:
        if flag not in not_delete:
            try:
                eval(f'{flag}.pop(message.chat.id)')
            except KeyError:
                pass


async def send_msg(message, text_user, text_admin, admins=('sourr_cream', 'sourr_cream')):
    clear_flags(message)
    await bot.send_message(chat_id=message.chat.id, text=text_user, parse_mode='html')
    for admin in admins:
        await bot.send_message(chat_id=config.ADMINS[admin], text=text_admin, parse_mode='html')




@bot.message_handler(commands=['start'])
async def basic_commands(message):
    models.db_object.db_insert(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='О нас'))
    markup.add(types.KeyboardButton(text='Услуги'))
    markup.add(types.KeyboardButton(text='Поддержка'))
    text = msg_text.RegularUser().start()
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    await services(message)


@bot.message_handler(commands=['admin'])
async def administration(message):
    ...


@bot.message_handler(content_types=['text'])
async def get_messages(message):
    if message.text == 'О нас':
        clear_flags(message)
        text = msg_text.base.about()
        await bot.send_message(chat_id=message.chat.id, text=text)
    elif message.text == 'Услуги':
        clear_flags(message)
        await services(message)
    elif message.text == 'Поддержка':
        msg_text.base.category[message.chat.id] = '<strong>Поддержка</strong>'
        clear_flags(message, not_delete=('msg_text.base.flag_support',))
        msg_text.base.flag_support[message.chat.id] = True
        text = msg_text.base.support_start()
        await bot.send_message(chat_id=message.chat.id, text=text)
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.dev_bots.finish(), text_admin=text_admin)
    elif msg_text.prom_tg.flag_prom_tg.get(message.chat.id):
        text_admin = f'{msg_text.base.category.get(message.chat.id)}\n' \
                     f'<strong>{msg_text.prom_tg.category.get(message.chat.id)}</strong>\n{message.text}'
        await send_msg(message=message, text_user=msg_text.prom_tg.finish(), admins=('sourr_cream',),  # qzark
                       text_admin=text_admin)
    elif msg_text.base.flag_support.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.base.support_finish(), text_admin=text_admin)
    elif msg_text.site.flag_sites.get(message.chat.id) or msg_text.design_obj.flag_design.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.dev_bots.finish(), text_admin=text_admin)
    elif msg_text.design_obj.flag_sup_brief.get(message.chat.id) or msg_text.site.flag_sup_brief.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.base.support_finish(), text_admin=text_admin)


async def services(message):
    text = msg_text.base.services()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Разработка чат-ботов', callback_data='develop_bots'))
    markup.add(types.InlineKeyboardButton(text='Реклама у блогеров', callback_data='bloggers'))
    markup.add(types.InlineKeyboardButton(text='Продвижение в телеграмм', callback_data='promotion_telegram'))
    markup.add(types.InlineKeyboardButton(text='Создание сайтов', callback_data='sites'))
    markup.add(types.InlineKeyboardButton(text='Дизайн', callback_data='design'))
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'develop_bots')
async def develop_bots(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Разработка чат-ботов</strong>'
    text = msg_text.dev_bots.start()
    msg_text.dev_bots.flag_develop_bots[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'bloggers')
async def bloggers(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Реклама у блогеров</strong>'
    ...


@bot.callback_query_handler(func=lambda callback: callback.data == 'promotion_telegram')
async def prom_telegram(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Продвижение в телеграмм</strong>'
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton(text='Рассылки в Telegram', callback_data='prom_tg_1'))
    markup.add(types.InlineKeyboardButton(text='Парсинг подписчиков', callback_data='prom_tg_2'))
    markup.add(types.InlineKeyboardButton(text='Инвайт в группы', callback_data='prom_tg_3'))
    markup.add(types.InlineKeyboardButton(text='PR компании', callback_data='prom_tg_4'))
    markup.add(types.InlineKeyboardButton(text='Циклические публикации в чатах',
                                          callback_data='prom_tg_5'))
    markup.add(types.InlineKeyboardButton(text='Посев нативных комментариев',
                                          callback_data='prom_tg_6'))
    text = msg_text.prom_tg.start()
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'prom_tg' in callback.data)
async def prom_telegram_2(callback):
    text = msg_text.prom_tg.prom_tg_markup()
    categories = {
                  '1': 'Рассылки в Telegram', '2': 'Парсинг подписчиков',
                  '3': 'Инвайт в группы', '4': 'PR компании',
                  '5': 'Циклические публикации в чатах', '6': 'Посев нативных комментариев'
                 }
    msg_text.prom_tg.category[callback.message.chat.id] = categories[callback.data.split('_')[-1]]
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'sites')
async def sites(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Создание сайтов</strong>'
    text = msg_text.site.start()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Заполнить бриф', callback_data='brief_site_1'))
    markup.add(types.InlineKeyboardButton(text='Нужна помощь специалиста',
                                          callback_data='brief_site_2'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'brief' in callback.data)
async def brief(callback):
    if callback.data.split('_')[-1] == '1':
        text = msg_text.site.fill_brief()
        document = config.DOCUMENT_SITE if 'site' in callback.data else config.DOCUMENT_DESIGN
        if 'site' in callback.data:
            msg_text.site.flag_sites[callback.message.chat.id] = True
            document = config.DOCUMENT_SITE
        elif 'design' in callback.data:
            msg_text.design_obj.flag_design[callback.message.chat.id] = True
            document = config.DOCUMENT_DESIGN
        with open(document, encoding='ISO-8859-1') as file:
            docx = file.read()
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)
        await bot.send_document(chat_id=callback.message.chat.id, document=docx)

    elif callback.data.split('_')[-1] == '2':
        msg_text.site.flag_sup_brief[callback.message.chat.id] = True
        msg_text.design_obj.flag_sup_brief[callback.message.chat.id] = True
        text = msg_text.site.sup_brief()
        msg_text.base.category[callback.message.chat.id] += '\n<strong>Нужна помощь специалиста</strong>'
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'design')
async def design(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Дизайн</strong>'
    text = msg_text.design_obj.start()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Заполнить бриф', callback_data='brief_design_1'))
    markup.add(types.InlineKeyboardButton(text='Нужна помощь специалиста',
                                          callback_data='brief_design_2'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text=text, reply_markup=markup)


@bot.message_handler(content_types=['document'])
async def get_docs(message):
    if msg_text.site.flag_sites.get(message.chat.id) or msg_text.design_obj.flag_design.get(message.chat.id):
        text = msg_text.site.finish()
        category = msg_text.base.category.get(message.chat.id)
        text_category = f'<strong>{category}</strong>\n'
        await bot.send_message(chat_id=message.chat.id, text=text)
        await bot.send_message(chat_id=config.ADMINS['sourr_cream'], text=text_category, parse_mode='html')  # qzark
        await bot.send_document(chat_id=config.ADMINS['sourr_cream'], document=message.document.file_id)  # qzark
        await bot.send_message(chat_id=config.ADMINS['sourr_cream'], text=text_category, parse_mode='html')  # decotto
        await bot.send_document(chat_id=config.ADMINS['sourr_cream'], document=message.document.file_id)  # decotto
    clear_flags(message)


async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())
