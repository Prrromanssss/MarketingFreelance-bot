import asyncio
import telebot.async_telebot
import config
import message as msg_text
from telebot import types
import markups
import models


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


'''Usual Functions'''


def clear_flags(message, callback=False, not_delete=()):
    if callback:
        message = message.message
    flags = (
             'msg_text.dev_bots.flag_develop_bots', 'msg_text.prom_tg.flag_prom_tg',
             'msg_text.prom_tg.category', 'msg_text.base.flag_support', 'msg_text.site.flag_sites',
             'msg_text.design_obj.flag_design', 'msg_text.site.flag_sup_brief',
             'msg_text.design_obj.flag_sup_brief', 'msg_text.design_obj.send_doc', 'msg_text.site.send_doc',
             'msg_text.blog.flag_for_bloggers', 'msg_text.blog.flag_network', 'msg_text.blog.flag_aim',
             'msg_text.blog.flag_budget', 'msg_text.admin.flag_for_password', 'msg_text.prom_tg.msg_for_delete'
             )
    for flag in flags:
        if flag not in not_delete:
            try:
                eval(f'{flag}.pop(message.chat.id)')
            except KeyError:
                pass


async def send_msg(message, text_user, text_admin=None, admins=('sourr_cream', 'sourr_cream'), markup=None):
    clear_flags(message)
    if markup:
        await bot.send_message(chat_id=message.chat.id, text=text_user, reply_markup=markup, parse_mode='html')
    else:
        await bot.send_message(chat_id=message.chat.id, text=text_user, parse_mode='html')
    text_admin = f'Юзернейм: @{models.db_object.db_select_user(message)}\n{text_admin}'
    for admin in admins:
        await bot.send_message(chat_id=config.ADMINS[admin], text=text_admin, parse_mode='html')


async def services(message):
    text = msg_text.base.services()
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.services_markup)


'''Command handlers'''


@bot.message_handler(commands=['start'])
async def basic_commands(message):
    models.db_object.db_insert(message)
    text = msg_text.reg_user.start()
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.main_markup)
    await services(message)


@bot.message_handler(commands=['admin'])
async def administration(message):
    await send_msg(message, text_user=msg_text.admin.write_password(), admins=())
    msg_text.admin.flag_for_password[message.chat.id] = True


'''Message handlers'''


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
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.admin_markup)
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
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.main_markup)
        await services(message)
    elif msg_text.admin.flag_for_newsletter.get(message.chat.id):
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            await bot.forward_message(chat_id[0], message.chat.id, message.message_id)
    elif message.text == 'Оплата услуг':
        clear_flags(message)
        text = msg_text.base.payment()
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.pay_service_markup)
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
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.continue_markup)
    elif message.text == '<< Назад' and msg_text.prom_tg.flag_prom_tg.get(message.chat.id):
        text = msg_text.prom_tg.start()
        await bot.delete_message(chat_id=message.chat.id, message_id=msg_text.prom_tg.msg_for_delete[message.chat.id].id)
        await bot.send_message(chat_id=message.chat.id, text=text,
                               reply_markup=markups.prom_tg_markup)
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id) and message.text != 'Далее':
        msg_text.base.category[message.chat.id] += f'\n{message.text}'
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id) and message.text == 'Далее':

        text_admin = msg_text.base.category.get(message.chat.id)
        await send_msg(message=message, text_user=msg_text.dev_bots.finish(), text_admin=text_admin,
                       markup=markups.main_markup)
    elif msg_text.prom_tg.flag_prom_tg.get(message.chat.id):
        text_admin = f'{msg_text.base.category.get(message.chat.id)}\n' \
                     f'<strong>{msg_text.prom_tg.category.get(message.chat.id)}</strong>\n{message.text}'
        await send_msg(message=message, text_user=msg_text.prom_tg.finish(), admins=('sourr_cream',),  # qzark
                       text_admin=text_admin)
    elif msg_text.base.flag_support.get(message.chat.id) and message.text != 'Далее':
        msg_text.base.category[message.chat.id] = msg_text.base.category.get(message.chat.id) + '\n' + message.text
    elif msg_text.base.flag_support.get(message.chat.id) and message.text == 'Далее':
        text_admin = msg_text.base.category[message.chat.id]
        await send_msg(message=message, text_user=msg_text.base.support_finish(),
                       text_admin=text_admin, markup=markups.clean_markup)
    elif msg_text.site.send_doc.get(message.chat.id) or msg_text.design_obj.send_doc.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.dev_bots.finish(), text_admin=text_admin)
    elif msg_text.design_obj.flag_sup_brief.get(message.chat.id) or msg_text.site.flag_sup_brief.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.base.support_finish(), text_admin=text_admin)
    elif msg_text.blog.flag_for_bloggers.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nЧто Вы хотите рекламировать: ' + message.text
        await send_msg(message, text_user=msg_text.blog.network(), admins=(), markup=markups.continue_markup)
        msg_text.blog.flag_network[message.chat.id] = True
    elif msg_text.blog.flag_network.get(message.chat.id) and message.text != 'Далее':
        if 'Расскажите подробнее, о вашем товаре/услуге?:' in msg_text.base.category[message.chat.id]:
            msg_text.base.category[message.chat.id] += message.text
        else:
            msg_text.base.category[message.chat.id] += '\nРасскажите подробнее, о вашем товаре/услуге?: '\
                                                       + message.text
    elif msg_text.blog.flag_network.get(message.chat.id) and message.text == 'Далее':
        if 'Расскажите подробнее, о вашем товаре/услуге?:' not in msg_text.base.category[message.chat.id]:
            msg_text.base.category[message.chat.id] += '\nРасскажите подробнее, о вашем товаре/услуге?: ' + '-'
        await send_msg(message, text_user=msg_text.blog.aim(), admins=())
        msg_text.blog.flag_aim[message.chat.id] = True
    elif msg_text.blog.flag_aim.get(message.chat.id) and message.text != 'Далее':
        if 'Кто является вашей целевой аудиторией:' in msg_text.base.category[message.chat.id]:
            msg_text.base.category[message.chat.id] += message.text
        else:
            msg_text.base.category[message.chat.id] += '\nКто является вашей целевой аудиторией: '\
                                                       + message.text
    elif msg_text.blog.flag_aim.get(message.chat.id) and message.text == 'Далее':
        if 'Кто является вашей целевой аудиторией:' not in msg_text.base.category[message.chat.id]:
            msg_text.base.category[message.chat.id] += '\nКто является вашей целевой аудиторией: ' + '-'
        await send_msg(message, text_user=msg_text.blog.budget(), admins=(), markup=markups.clean_markup)
        msg_text.blog.flag_budget[message.chat.id] = True
    elif msg_text.blog.flag_budget.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nКакой у Вас рекламный бюджет: ' + message.text
        await send_msg(message, text_user=msg_text.blog.finish(), text_admin=msg_text.base.category[message.chat.id],
                       markup=markups.clean_markup)
    elif msg_text.admin.flag_for_password.get(message.chat.id):
        if config.ADMIN_PASSWORD == message.text:
            clear_flags(message)
            await bot.send_message(chat_id=message.chat.id, text=msg_text.admin.start(),
                                   reply_markup=markups.admin_markup)
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


@bot.message_handler(content_types=['successful_payment'])
async def process_pay(message):
    if message.successful_payment.invoice_payload == 'payment_service':
        text = msg_text.base.success_pay()
        await bot.send_message(chat_id=message.chat.id, text=text)


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


'''Payments handlers'''


@bot.pre_checkout_query_handler(func=lambda query: True)
async def process_pre_checkout_query(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


'''Callback handlers'''


@bot.callback_query_handler(func=lambda callback: callback.data == 'develop_bots')
async def develop_bots(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Разработка чат-ботов</strong>'
    text = msg_text.dev_bots.start()
    msg_text.dev_bots.flag_develop_bots[callback.message.chat.id] = True
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await bot.send_message(chat_id=callback.message.chat.id,
                           text=text, reply_markup=markups.continue_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'bloggers')
async def bloggers(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Реклама у блогеров</strong>'
    text = msg_text.blog.start()
    msg_text.blog.flag_for_bloggers[callback.message.chat.id] = True

    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text=text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'promotion_telegram')
async def prom_telegram(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Продвижение в телеграмм</strong>'
    text = msg_text.prom_tg.start()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                reply_markup=markups.prom_tg_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_1')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_2')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_3')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_4')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_5')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_6')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_7')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegram()
    await general_prom_tg(callback, text)


async def general_prom_tg(callback, text):
    msg_text.prom_tg.category[callback.message.chat.id] = msg_text.prom_tg.all_categories[callback.data.split('_')[-1]]
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    msg = await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=markups.back_markup)
    msg_text.prom_tg.msg_for_delete[callback.message.chat.id] = msg


@bot.callback_query_handler(func=lambda callback: callback.data == 'sites')
async def sites(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Создание сайтов</strong>'
    text = msg_text.site.start()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text=text, reply_markup=markups.brief_site_markup)


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
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text=text, reply_markup=markups.brief_design_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'pay_service')
async def payment_of_services(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await bot.send_invoice(chat_id=callback.message.chat.id, title='Оплата услуг',
                           description='Тестовое описание товара', invoice_payload='payment_service',
                           provider_token=config.YOO_TOKEN, currency='RUB', start_parameter='MarketingFreelance_bot',
                           prices=[types.LabeledPrice(label='Оплата услуг', amount='100000')])


async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())
