import asyncio
import telebot.async_telebot
import config
import message as msg_text
from telebot import types
import markups
import models


bot = telebot.async_telebot.AsyncTeleBot(config.BOT_TOKEN)


'''Usual Functions'''


def clear_admin_flags(message):
    flags = (
             'msg_text.admin.flag_for_write_user', 'msg_text.admin.flag_for_newsletter', 'msg_text.admin.user_to_send',
             'msg_text.admin.flag_for_private_msg', 'msg_text.admin.msg_to_send'
    )
    for flag in flags:
        try:
            eval(f'{flag}.pop(message.chat.id)')
        except KeyError:
            pass


def clear_flags(message, callback=False, not_delete=()):
    if callback:
        message = message.message
    flags = (
             'msg_text.dev_bots.flag_develop_bots', 'msg_text.prom_tg.flag_prom_tg',
             'msg_text.prom_tg.category', 'msg_text.base.flag_support', 'msg_text.site.flag_sites',
             'msg_text.design_obj.flag_design', 'msg_text.site.flag_sup_brief',
             'msg_text.design_obj.flag_sup_brief', 'msg_text.design_obj.send_doc', 'msg_text.site.send_doc',
             'msg_text.blog.flag_for_bloggers', 'msg_text.blog.flag_detail_product', 'msg_text.blog.flag_aim',
             'msg_text.blog.flag_budget', 'msg_text.admin.flag_for_password', 'msg_text.prom_tg.msg_for_delete',
             'msg_text.prom_tg.flag_prom_tg', 'msg_text.prom_tg.newsletter', 'msg_text.prom_tg.number_newsletter',
             'msg_text.prom_tg.complex_href', 'msg_text.prom_tg.complex_contact'
             )
    for flag in flags:
        if flag not in not_delete:
            try:
                eval(f'{flag}.pop(message.chat.id)')
            except KeyError:
                pass


async def send_msg(message, text_user, text_admin=None, admins=('qzark', 'zakazy'), markup=None):
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
    """Handler to process text message"""

    '''This coroutine process all text message using flags'''

    # ---------------------------
    #   Administration basement
    # ---------------------------

    # Base to start sending out messages to all users
    if msg_text.admin.flag_account.get(message.chat.id) and message.text == 'Рассылки сообщений':
        clear_admin_flags(message)
        msg_text.admin.flag_for_newsletter[message.chat.id] = True
        text = msg_text.admin.newsletter()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text='Стоп'))
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

    # Sending out messages to all users
    elif msg_text.admin.flag_for_newsletter.get(message.chat.id) and message.text != 'Стоп':
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            if message.text:
                await bot.send_message(chat_id=chat_id[0], text=message.text)

    # Base to stop send out messages to users and to go over to main menu
    elif (msg_text.admin.flag_account.get(message.chat.id) and msg_text.admin.flag_for_newsletter.get(message.chat.id)
            and message.text == 'Стоп'):
        clear_admin_flags(message)
        text = msg_text.admin.success_newsletter()
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.admin_markup)

    # Base to send a user to whom to send message
    elif msg_text.admin.flag_account.get(message.chat.id) and message.text == 'Личное сообщение от бота':
        clear_admin_flags(message)
        msg_text.admin.flag_for_write_user[message.chat.id] = True
        text = msg_text.admin.write_username()
        await bot.send_message(chat_id=message.chat.id, text=text)

    # Getting the user to send private message
    elif msg_text.admin.flag_account.get(message.chat.id) and msg_text.admin.flag_for_write_user.get(message.chat.id):
        clear_admin_flags(message)
        text = msg_text.admin.send_private()
        msg_text.admin.flag_for_private_msg[message.chat.id] = True
        msg_text.admin.user_to_send[message.chat.id] = message.text
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.continue_markup)

    # Sending private message to user
    elif msg_text.admin.flag_for_private_msg.get(message.chat.id) and msg_text.admin.flag_account.get(message.chat.id):
        if message.text != 'Далее':
            msg_text.admin.msg_to_send[message.chat.id] = msg_text.admin.msg_to_send.get(message.chat.id, '') + '\n'\
                                                          + message.text
        else:
            text = msg_text.admin.success_sending_private()
            try:
                user_id = models.db_object.db_select_user_id(msg_text.admin.user_to_send[message.chat.id][1:])
            except Exception:
                text = msg_text.admin.user_not_found()
                await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.admin_markup)
                clear_admin_flags(message)
                return
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.admin_markup)
            await bot.send_message(chat_id=user_id,
                                   text=msg_text.admin.msg_to_send[message.chat.id])
            clear_admin_flags(message)

    # Base to see all users subscribed to bot
    elif msg_text.admin.flag_account.get(message.chat.id) and message.text == 'Просмотр всех пользователей':
        usernames = models.db_object.db_select_all_users()

        text = ''
        for user in usernames:
            text += f'<strong>Юзернейм:</strong> @{user[0]}\n'
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html')

    # Base to return to usual user's account
    elif msg_text.admin.flag_account.get(message.chat.id) and message.text == '<< Вернуться назад':
        del msg_text.admin.flag_account[message.chat.id]
        clear_flags(message)
        text = msg_text.admin.finish()
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.main_markup)
        await services(message)

    # -----------------------
    #   Usual user basement
    # -----------------------

    # Base to see variants of payments
    elif message.text == 'Оплата услуг':
        clear_flags(message)
        text = msg_text.base.payment()
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.href_service_markup)

    # Base to know about us
    elif message.text == 'О нас':
        clear_flags(message)
        text = msg_text.base.about()
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html')

    # Base to go over to services we provide
    elif message.text == 'Услуги':
        clear_flags(message)
        await services(message)

    # Base to start texting message to support
    elif message.text == 'Поддержка':
        msg_text.base.category[message.chat.id] = '<strong>Поддержка</strong>'
        clear_flags(message, not_delete=('msg_text.base.flag_support',))
        msg_text.base.flag_support[message.chat.id] = True
        text = msg_text.base.support_start()
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.continue_markup)

    # Texting message to support
    elif msg_text.base.flag_support.get(message.chat.id):
        if message.text != 'Далее':
            msg_text.base.category[message.chat.id] = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        else:
            text_admin = msg_text.base.category[message.chat.id]
            await send_msg(message=message, text_user=msg_text.base.support_finish(),
                           text_admin=text_admin, markup=markups.main_markup)

    # ------------------------------
    #   Service of developing bots
    # ------------------------------

    # Processing incoming messages and sending them to admins
    elif msg_text.dev_bots.flag_develop_bots.get(message.chat.id):
        if message.text != 'Далее':
            msg_text.base.category[message.chat.id] += f'\n{message.text}'
        else:
            text_admin = msg_text.base.category[message.chat.id]
            await send_msg(message=message, text_user=msg_text.dev_bots.finish(),
                           text_admin=text_admin, markup=markups.main_markup)

    # -------------------------------
    #   Service of ad from bloggers
    # -------------------------------

    # The answer from the first question
    elif msg_text.blog.flag_for_bloggers.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nЧто Вы хотите рекламировать: ' + message.text
        await send_msg(message, text_user=msg_text.blog.detail_product(), admins=(), markup=markups.continue_markup)
        msg_text.blog.flag_detail_product[message.chat.id] = True

    # The answer from the second question
    elif msg_text.blog.flag_detail_product.get(message.chat.id):
        if message.text != 'Далее':
            if 'Расскажите подробнее, о вашем товаре/услуге?:' in msg_text.base.category[message.chat.id]:
                msg_text.base.category[message.chat.id] += '  ' + message.text
            else:
                msg_text.base.category[message.chat.id] += '\nРасскажите подробнее, о вашем товаре/услуге?: '\
                                                           + message.text
        else:
            if 'Расскажите подробнее, о вашем товаре/услуге?:' not in msg_text.base.category[message.chat.id]:
                msg_text.base.category[message.chat.id] += '\nРасскажите подробнее, о вашем товаре/услуге?: ' + '-'
            await send_msg(message, text_user=msg_text.blog.aim(), admins=())
            msg_text.blog.flag_aim[message.chat.id] = True

    # The answer from the third question
    elif msg_text.blog.flag_aim.get(message.chat.id):
        if message.text != 'Далее':
            if 'Кто является вашей целевой аудиторией:' in msg_text.base.category[message.chat.id]:
                msg_text.base.category[message.chat.id] += '   ' + message.text
            else:
                msg_text.base.category[message.chat.id] += '\nКто является вашей целевой аудиторией: '\
                                                           + message.text
        else:
            if 'Кто является вашей целевой аудиторией:' not in msg_text.base.category[message.chat.id]:
                msg_text.base.category[message.chat.id] += '\nКто является вашей целевой аудиторией: ' + '-'
            await send_msg(message, text_user=msg_text.blog.budget(), admins=(), markup=markups.clean_markup)
            msg_text.blog.flag_budget[message.chat.id] = True

    # The answer from the fourth question
    elif msg_text.blog.flag_budget.get(message.chat.id):
        msg_text.base.category[message.chat.id] += '\nКакой у Вас рекламный бюджет: ' + message.text
        await send_msg(message, text_user=msg_text.blog.finish(), text_admin=msg_text.base.category[message.chat.id],
                       markup=markups.main_markup)

    # ---------------------------------
    #   Service of promotion telegram
    # ---------------------------------

    # Base to go over to main menu of promotion telegram
    elif message.text == '<< Назад' and msg_text.prom_tg.flag_prom_tg.get(message.chat.id):
        text = msg_text.prom_tg.start()

        msg_text.base.category[message.chat.id] = '\n'.join(msg_text.base.category[message.chat.id].split('\n')[:1])

        await bot.delete_message(chat_id=message.chat.id, message_id=msg_text.prom_tg.msg_for_delete[message.chat.id].id)
        await bot.send_message(chat_id=message.chat.id, text=text,
                               reply_markup=markups.prom_tg_markup)

    # Invite to groups from service of promotion telegram / Parsing subscribers / PR-company
    elif msg_text.prom_tg.flag_prom_tg.get(message.chat.id) and message.text != '<< Назад':
        if message.text != 'Далее':
            msg_text.base.category[message.chat.id] += f'\n{message.text}'
        else:
            text_admin = msg_text.base.category[message.chat.id]
            await send_msg(message, text_user=msg_text.ListPromotionTelegramInvite().finish(),
                           text_admin=text_admin, markup=markups.main_markup)

    # Newsletter in Telegram
    elif msg_text.prom_tg.newsletter.get(message.chat.id):
        if message.text != 'Далее':
            msg_text.base.category[message.chat.id] += f'\n{message.text}'
        else:
            text = msg_text.ListPromotionTelegramNewsletter().number()
            await send_msg(message, text_user=text, admins=(), markup=markups.prom_tg_newsletter_number_markup)

    # Complex to get href from promotion telegram
    elif msg_text.prom_tg.complex_href.get(message.chat.id):
        text = msg_text.ListPromotionTelegramComplex().contact()
        msg_text.base.category[message.chat.id] += '\nСсылка на проект: ' + f'{message.text}'
        await send_msg(message, text_user=text, admins=())
        msg_text.prom_tg.complex_contact[message.chat.id] = True

    # Complex to get contact from promotion telegram
    elif msg_text.prom_tg.complex_contact.get(message.chat.id):
        text = msg_text.ListPromotionTelegramComplex().finish()
        msg_text.base.category[message.chat.id] += '\nКонтакты: ' + f'{message.text}'
        text_admin = msg_text.base.category[message.chat.id]
        await send_msg(message, text_user=text, text_admin=text_admin, markup=markups.main_markup)

    # ------------------------------------------------------------------------
    #   Service of creating sites and design (they have the same functional)
    # ------------------------------------------------------------------------

    # Processing brief
    elif msg_text.site.send_doc.get(message.chat.id) or msg_text.design_obj.send_doc.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.site.finish(), text_admin=text_admin)

    # Appeal to support
    elif msg_text.design_obj.flag_sup_brief.get(message.chat.id) or msg_text.site.flag_sup_brief.get(message.chat.id):
        text_admin = msg_text.base.category.get(message.chat.id) + '\n' + message.text
        await send_msg(message=message, text_user=msg_text.base.support_finish(), text_admin=text_admin,
                       markup=markups.main_markup)

    # --------------------------
    #   Enter to admin account
    # --------------------------

    # Compare input to password
    elif msg_text.admin.flag_for_password.get(message.chat.id):
        if config.ADMIN_PASSWORD == message.text:
            clear_flags(message)
            await bot.send_message(chat_id=message.chat.id, text=msg_text.admin.start(),
                                   reply_markup=markups.admin_markup)
            msg_text.admin.flag_account[message.chat.id] = True
        else:
            await send_msg(message, text_user=msg_text.admin.password_false(), admins=())

    # ------------------
    #   Another cases
    # -----------------

    # Unknown message
    else:
        await send_msg(message=message, text_user=msg_text.base.unknown(), admins=())


@bot.message_handler(content_types=config.CONTENT_TYPES)
async def newsletter(message):
    if msg_text.admin.flag_for_newsletter.get(message.chat.id):
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            if message.sticker:
                await bot.send_sticker(chat_id=chat_id[0], sticker=message.sticker.file_id)
            if message.photo:
                await bot.send_photo(chat_id=chat_id[0], photo=message.json['photo'][0]['file_id'])
            if message.location and not message.venue:
                await bot.send_location(chat_id=chat_id[0], longitude=message.location.longitude,
                                        latitude=message.location.latitude)
            if message.venue:
                await bot.send_venue(chat_id=chat_id[0], longitude=message.location.longitude,
                                     latitude=message.location.latitude, title=message.venue.title,
                                     address=message.venue.address)
            if message.video:
                await bot.send_video(chat_id=chat_id[0], video=message.video.file_id,
                                     )
            if message.voice:
                await bot.send_voice(chat_id=chat_id[0], voice=message.voice.file_id)
            if message.contact:
                await bot.send_contact(chat_id=chat_id[0], phone_number=message.contact.phone_number,
                                       first_name=message.contact.first_name,
                                       last_name=message.contact.last_name)


@bot.message_handler(content_types=['document'])
async def get_docs(message):
    if msg_text.site.flag_sites.get(message.chat.id) or msg_text.design_obj.flag_design.get(message.chat.id):
        msg_text.site.send_doc[message.chat.id] = True
        msg_text.design_obj.send_doc[message.chat.id] = True
        text_user = msg_text.site.finish()
        category = msg_text.base.category.get(message.chat.id)
        text_category = f'<strong>{category}</strong>\n'
        await send_msg(message, text_user=text_user, text_admin=text_category, markup=markups.main_markup)
        await bot.send_document(chat_id=config.ADMINS['qzark'], document=message.document.file_id)  # qzark
        await bot.send_document(chat_id=config.ADMINS['zakazy'], document=message.document.file_id)  # zakazy

    elif msg_text.admin.flag_for_newsletter.get(message.chat.id):
        users_id = models.db_object.db_select_all_users_id()
        for chat_id in users_id:
            if message.document:
                await bot.send_document(chat_id=chat_id[0], document=message.document.file_id)
    else:
        await send_msg(message=message, text_user=msg_text.base.unknown(), admins=())
    clear_flags(message)


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
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await bot.send_message(chat_id=callback.message.chat.id,
                           text=text, reply_markup=markups.clean_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'promotion_telegram')
async def prom_telegram(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Продвижение в телеграмм</strong>'
    text = msg_text.prom_tg.start()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                reply_markup=markups.prom_tg_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_1')
async def prom_tg_newsletter(callback):
    text = msg_text.ListPromotionTelegramNewsletter().start()
    await general_prom_tg(callback, text_start=text, markup=markups.prom_tg_newsletter_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_1_want')
async def prom_tg_newsletter_want(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    msg_text.prom_tg.newsletter[callback.message.chat.id] = True
    text = msg_text.ListPromotionTelegramNewsletter().press_yes()
    await bot.send_message(chat_id=callback.message.chat.id, text=text,
                           reply_markup=markups.back_continue_markup)


@bot.callback_query_handler(func=lambda callback: 'prom_tg_1_number' in callback.data)
async def prom_tg_newsletter_number(callback):
    numbers = {'1': '1000', '2': '2000', '3': '3000', '4': '5000', '5': '10000'}
    if callback.data.split('_')[-1] == '6' and 'inp' not in callback.data:
        text = msg_text.ListPromotionTelegramNewsletter().number() + '\n' + 'Количество: '

        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markups.prom_tg_newsletter_inp_number_markup)
    elif 'inp' in callback.data:
        msg_text.prom_tg.number_newsletter[callback.message.chat.id] = msg_text.prom_tg.number_newsletter.get(callback.message.chat.id, '')\
                                                           + callback.data.split('_')[-1]
        text = msg_text.ListPromotionTelegramNewsletter().number() + '\n' + 'Количество: '\
                                                                   + msg_text.prom_tg.number_newsletter[callback.message.chat.id]
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text=text,
                                    reply_markup=markups.prom_tg_newsletter_inp_last_number_markup)
    else:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        if 'last' in callback.data:
            msg_text.base.category[callback.message.chat.id] += '\nКоличество сообщений: '\
                                                             + msg_text.prom_tg.number_newsletter[callback.message.chat.id]
        else:
            msg_text.base.category[callback.message.chat.id] += '\nКоличество сообщений: '\
                                                                + numbers[callback.data.split('_')[-1]]
        text_user = msg_text.ListPromotionTelegramNewsletter().finish()
        text_admin = msg_text.base.category.get(callback.message.chat.id)
        await send_msg(callback.message, text_user=text_user, text_admin=text_admin, markup=markups.main_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_1_sup')
async def prom_tg_newsletter_support(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    msg_text.base.category[callback.message.chat.id] += f'\nНужна ваша помощь'
    text = msg_text.ListPromotionTelegramNewsletter().finish()
    await send_msg(callback.message, text_user=text, text_admin=msg_text.base.category[callback.message.chat.id])


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_2')
async def prom_tg_invite(callback):
    text = msg_text.ListPromotionTelegramInvite().start()
    await general_prom_tg(callback, text_start=text, markup=markups.prom_tg_invite_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_2_want')
async def prom_tg_invite_want(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    text = msg_text.ListPromotionTelegramInvite().press_yes()
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    msg_text.base.category[callback.message.chat.id] += '\n<strong>Инвайт в группы</strong>'
    msg = await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=markups.back_continue_markup)
    msg_text.prom_tg.msg_for_delete[callback.message.chat.id] = msg


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_3')
async def prom_tg_parsing(callback):
    text = msg_text.ListPromotionTelegramParsing().start()
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    msg_text.base.category[callback.message.chat.id] += '\n<strong>Парсинг подписчиков</strong>'
    await general_prom_tg(callback, text_start=text, markup=markups.back_continue_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_4')
async def prom_tg_pr(callback):
    text = msg_text.ListPromotionTelegramPR().start()
    msg_text.prom_tg.flag_prom_tg[callback.message.chat.id] = True
    msg_text.base.category[callback.message.chat.id] += '\n<strong>PR компании</strong>'

    await general_prom_tg(callback, text_start=text, markup=markups.back_continue_markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['prom_tg_5', 'prom_tg_6'])
async def prom_tg_cycle_comments(callback):
    if callback.data == 'prom_tg_5':
        msg_text.base.category[callback.message.chat.id] += '\n<strong>Циклические публикации в чатах</strong>'
        text = msg_text.ListPromotionTelegramCycle().start()
    else:
        msg_text.base.category[callback.message.chat.id] += '\n<strong>Посев нативных комментариев</strong>'
        text = msg_text.ListPromotionTelegramComments().start()
    await general_prom_tg(callback, text_start=text, markup=markups.prom_tg_cycle_comments_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_5_6_want')
async def prom_tg_cycle_comments_want(callback):
    msg_text.base.category[callback.message.chat.id] += '\nКлиент хочет заказать услугу'
    text = msg_text.ListPromotionTelegramCycle().finish()
    text_admin = msg_text.base.category.get(callback.message.chat.id)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await send_msg(callback.message, text_user=text, text_admin=text_admin)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_7')
async def prom_tg_complex(callback):
    text = msg_text.ListPromotionTelegramComplex().start()
    await general_prom_tg(callback, text_start=text, markup=markups.prom_tg_complex_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'prom_tg_7_want')
async def prom_tg_complex_want(callback):
    msg_text.base.category[callback.message.chat.id] += '\nКлиент хочет заказать консультацию'
    text = msg_text.ListPromotionTelegramComplex().href()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await send_msg(callback.message, text_user=text, admins=())
    msg_text.prom_tg.complex_href[callback.message.chat.id] = True


async def general_prom_tg(callback, text_start, markup=None):
    msg_text.prom_tg.category[callback.message.chat.id] = msg_text.prom_tg.all_categories[callback.data.split('_')[-1]]

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    if markup:
        msg = await bot.send_message(chat_id=callback.message.chat.id, text=text_start,
                                     reply_markup=markup, parse_mode='html')
    else:
        msg = await bot.send_message(chat_id=callback.message.chat.id, text=text_start, parse_mode='html')

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
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=markups.clean_markup)
        await bot.send_document(chat_id=callback.message.chat.id, document=document)
    elif callback.data.split('_')[-1] == '2':
        msg_text.site.flag_sup_brief[callback.message.chat.id] = True
        msg_text.design_obj.flag_sup_brief[callback.message.chat.id] = True
        text = msg_text.site.sup_brief()
        msg_text.base.category[callback.message.chat.id] += '\n<strong>Нужна помощь специалиста</strong>'
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        await bot.send_message(chat_id=callback.message.chat.id, text=text, reply_markup=markups.clean_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'design')
async def design(callback):
    msg_text.base.category[callback.message.chat.id] = f'<strong>Дизайн</strong>'
    text = msg_text.design_obj.start()
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                                text=text, reply_markup=markups.brief_design_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'back_service')
async def back_to_services(callback):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    await services(callback.message)


async def main():
    await asyncio.gather(bot.polling(
                                    interval=1,
                                    non_stop=True,
                                    request_timeout=1000,
                                    timeout=1000
                                    ))


if __name__ == '__main__':
    asyncio.run(main())
