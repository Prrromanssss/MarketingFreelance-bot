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
             'msg_text.prom_tg.category', 'msg_text.base.flag_support', 'msg_text.site.flag_sites',
             'msg_text.design_obj.flag_design', 'msg_text.site.flag_sup_brief',
             'msg_text.design_obj.flag_sup_brief', 'msg_text.design_obj.send_doc', 'msg_text.site.send_doc',
             'msg_text.blog.flag_for_bloggers', 'msg_text.blog.flag_network', 'msg_text.blog.flag_aim',
             'msg_text.blog.flag_budget', 'msg_text.admin.flag_for_password',
             )
    for flag in flags:
        if flag not in not_delete:
            try:
                eval(f'{flag}.pop(message.chat.id)')
            except KeyError:
                pass


async def send_msg(message, text_user, text_admin=None, admins=('sourr_cream', 'sourr_cream'), is_markup=False):
    clear_flags(message)
    if is_markup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='О нас'))
        markup.add(types.KeyboardButton(text='Услуги'))
        markup.add(types.KeyboardButton(text='Оплатить услуги'))
        markup.add(types.KeyboardButton(text='Поддержка'))
        await bot.send_message(chat_id=message.chat.id, text=text_user, reply_markup=markup, parse_mode='html')
    else:
        await bot.send_message(chat_id=message.chat.id, text=text_user, parse_mode='html')
    text_admin = f'Юзернейм: @{models.db_object.db_select_user(message)}\n{text_admin}'
    for admin in admins:
        await bot.send_message(chat_id=config.ADMINS[admin], text=text_admin, parse_mode='html')


@bot.message_handler(commands=['start'])
async def basic_commands(message):
    models.db_object.db_insert(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='О нас'))
    markup.add(types.KeyboardButton(text='Услуги'))
    markup.add(types.KeyboardButton(text='Оплатить услуги'))
    markup.add(types.KeyboardButton(text='Поддержка'))
    text = msg_text.RegularUser().start()
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    await services(message)


@bot.message_handler(commands=['admin'])
async def administration(message):
    await send_msg(message, text_user=msg_text.admin.write_password(), admins=())
    msg_text.admin.flag_for_password[message.chat.id] = True


@bot.message_handler(content_types=['text'])
async def get_messages(message):
    if msg_text.admin.flag_account.get(message.chat.id) and message.text == 'Рассылки сообщений':
        msg_text.admin.flag_for_newsletter[message.chat.id] = True
        text = msg_text.admin.newsletter()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Стоп'))
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    elif (msg_text.admin.flag_account.get(message.chat.id) and msg_text.admin.flag_for_newsletter.get(message.chat.id)
            and message.text == 'Стоп'):
        del msg_text.admin.flag_for_newsletter[message.chat.id]
        text = msg_text.admin.success_newsletter()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Рассылки сообщений'))
        markup.add(types.KeyboardButton(text='Просмотр всех пользователей'))
        markup.add(types.KeyboardButton(text='<< Вернуться назад'))
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
    elif msg_text.admin.flag_account.get(message.chat.id) and message.text == 'Просмотр всех пользователей':
        usernames = models.db_object.db_select_all_users()
        text = ''
        for user in usernames:
            text += f'<strong>Юзернейм:</strong> @{user[0]}\n'
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html')
    elif msg_text.admin.flag_account.get(message.chat.id) and message.text == '<< Вернуться назад':
        del msg_text.admin.flag_account[message.chat.id]
        clear_flags(message)
        text = msg_text.admin.finish()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='О нас'))
        markup.add(types.KeyboardButton(text='Услуги'))
        markup.add(types.KeyboardButton(text='Оплатить услуги'))
        markup.add(types.KeyboardButton(text='Поддержка'))
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
        await services(message)
    elif msg_text.admin.flag_for_newsletter.get(message.chat.id):
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            await bot.forward_message(chat_id[0], message.chat.id, message.message_id)
    elif message.text == 'Оплатить услуги':
        clear_flags(message)
        text = msg_text.base.payment()
        await bot.send_message(chat_id=message.chat.id, text=text)
        await bot.send_invoice(chat_id=message.chat.id, title='Оплата услуг', description='Тестовое описание товара',
                               invoice_payload='payment_service', provider_token=config.YOO_TOKEN, currency='RUB',
                               start_parameter='MarketingFreelance_bot',
                               prices=[types.LabeledPrice(label='Оплата услуг', amount='1000')])
    elif message.text == 'О нас':
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
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id) and message.text != 'Всё':
        msg_text.base.category[message.chat.id] += f'\n{message.text}'
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id) and message.text == 'Всё':
        text_admin = msg_text.base.category.get(message.chat.id)
        await send_msg(message=message, text_user=msg_text.dev_bots.finish(), text_admin=text_admin, is_markup=True)
    elif msg_text.prom_tg.flag_prom_tg.get(message.chat.id):
        text_admin = f'{msg_text.base.category.get(message.chat.id)}\n' \
                     f'<strong>{msg_text.prom_tg.category.get(message.chat.id)}</strong>\n{message.text}'
        await send_msg(message=message, text_user=msg_text.prom_tg.finish(), admins=('sourr_cream',),  # qzark
                       text_admin=text_admin)
    elif msg_text.base.flag_support.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.base.support_finish(), text_admin=text_admin)
    elif msg_text.site.send_doc.get(message.chat.id) or msg_text.design_obj.send_doc.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.dev_bots.finish(), text_admin=text_admin)
    elif msg_text.design_obj.flag_sup_brief.get(message.chat.id) or msg_text.site.flag_sup_brief.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.base.support_finish(), text_admin=text_admin)
    elif msg_text.blog.flag_for_bloggers.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nЧто Вы хотите рекламировать: ' + message.text
        await send_msg(message, text_user=msg_text.blog.network(), admins=())
        msg_text.blog.flag_network[message.chat.id] = True
    elif msg_text.blog.flag_network.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nВ какой социальной сети: ' + message.text
        await send_msg(message, text_user=msg_text.blog.aim(), admins=())
        msg_text.blog.flag_aim[message.chat.id] = True
    elif msg_text.blog.flag_aim.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nКто является вашей целевой аудиторией: ' + message.text
        await send_msg(message, text_user=msg_text.blog.budget(), admins=())
        msg_text.blog.flag_budget[message.chat.id] = True
    elif msg_text.blog.flag_budget.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nКакой у Вас рекламный бюджет: ' + message.text
        await send_msg(message, text_user=msg_text.blog.finish(), text_admin=msg_text.base.category[message.chat.id])
    elif msg_text.admin.flag_for_password.get(message.chat.id):
        if config.ADMIN_PASSWORD == message.text:
            clear_flags(message)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(text='Рассылки сообщений'))
            markup.add(types.KeyboardButton(text='Просмотр всех пользователей'))
            markup.add(types.KeyboardButton(text='<< Вернуться назад'))

            await bot.send_message(chat_id=message.chat.id, text=msg_text.admin.start(), reply_markup=markup)
            msg_text.admin.flag_account[message.chat.id] = True
        else:
            await send_msg(message, text_user=msg_text.admin.password_false(), admins=())
    else:
        await send_msg(message=message, text_user=msg_text.base.unknown(), admins=())


@bot.message_handler(content_types=config.CONTENT_TYPES)
async def newsletter(message):
    if msg_text.admin.flag_for_newsletter.get(message.chat.id):
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            await bot.forward_message(chat_id[0], message.chat.id, message.message_id)


async def services(message):
    text = msg_text.base.services()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Разработка чат-ботов', callback_data='develop_bots'))
    markup.add(types.InlineKeyboardButton(text='Реклама у блогеров', callback_data='bloggers'))
    markup.add(types.InlineKeyboardButton(text='Продвижение в телеграмм', callback_data='promotion_telegram'))
    markup.add(types.InlineKeyboardButton(text='Создание сайтов', callback_data='sites'))
    markup.add(types.InlineKeyboardButton(text='Дизайн', callback_data='design'))
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.pre_checkout_query_handler(func=lambda query: True)
async def process_pre_checkout_query(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
async def process_pay(message):
    if message.successful_payment.invoice_payload == 'payment_service':
        text = msg_text.base.success_pay()
        await bot.send_message(chat_id=message.chat.id, text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'develop_bots')
async def develop_bots(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Разработка чат-ботов</strong>'
    text = msg_text.dev_bots.start()
    msg_text.dev_bots.flag_develop_bots[callback.message.chat.id] = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text='Всё'))
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await bot.send_message(chat_id=callback.message.chat.id,
                                text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'bloggers')
async def bloggers(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Реклама у блогеров</strong>'
    text = msg_text.blog.start()
    msg_text.blog.flag_for_bloggers[callback.message.chat.id] = True
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)


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
        if 'site' in callback.data:
            msg_text.site.flag_sites[callback.message.chat.id] = True
            document = config.SITE_HASH_FILE_ID
        elif 'design' in callback.data:
            msg_text.design_obj.flag_design[callback.message.chat.id] = True
            document = config.DESIGN_HASH_FILE_ID
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text)
        await bot.send_document(chat_id=callback.message.chat.id, document=document)

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
        msg_text.site.send_doc[message.chat.id] = True
        msg_text.design_obj.send_doc[message.chat.id] = True
        text = msg_text.site.finish()
        category = msg_text.base.category.get(message.chat.id)
        text_category = f'<strong>{category}</strong>\n'

        await send_msg(message, text_user=text, text_admin=text_category)
        await bot.send_document(chat_id=config.ADMINS['sourr_cream'], document=message.document.file_id)  # qzark
        await bot.send_document(chat_id=config.ADMINS['sourr_cream'], document=message.document.file_id)  # decotto
    elif msg_text.admin.flag_for_newsletter.get(message.chat.id):
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            await bot.forward_message(chat_id[0], message.chat.id, message.message_id)
    else:
        await send_msg(message=message, text_user=msg_text.base.unknown(), admins=())
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
