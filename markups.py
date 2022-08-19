from telebot import types

'''-------------------'''
'''ReplyKeyboardMarkup'''
'''-------------------'''

'''clean_markup'''
clean_markup = types.ReplyKeyboardRemove()

'''main markup'''
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add(types.KeyboardButton(text='О нас'))
main_markup.add(types.KeyboardButton(text='Услуги'))
main_markup.add(types.KeyboardButton(text='Оплата услуг'))
main_markup.add(types.KeyboardButton(text='Поддержка'))

'''continue markup'''
continue_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
continue_markup.add(types.KeyboardButton(text='Далее'))

'''admin markup'''
admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_markup.add(types.KeyboardButton(text='Рассылки сообщений'))
admin_markup.add(types.KeyboardButton(text='Просмотр всех пользователей'))
admin_markup.add(types.KeyboardButton(text='Личное сообщение от бота'))
admin_markup.add(types.KeyboardButton(text='<< Вернуться назад'))

'''back markup'''
back_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_markup.add(types.KeyboardButton(text='<< Назад'))

'''back markup with continue markup'''
back_continue_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_continue_markup.add(types.KeyboardButton(text='Далее'))
back_continue_markup.add(types.KeyboardButton(text='<< Назад'))

'''--------------------'''
'''InlineKeyboardMarkup'''
'''--------------------'''

'''services markup '''
services_markup = types.InlineKeyboardMarkup()
services_markup.add(types.InlineKeyboardButton(text='Разработка чат-ботов', callback_data='develop_bots'))
services_markup.add(types.InlineKeyboardButton(text='Реклама у блогеров', callback_data='bloggers'))
services_markup.add(types.InlineKeyboardButton(text='Продвижение в телеграмм', callback_data='promotion_telegram'))
services_markup.add(types.InlineKeyboardButton(text='Создание сайтов', callback_data='sites'))
services_markup.add(types.InlineKeyboardButton(text='Дизайн', callback_data='design'))

'''promotion telegram markup'''
prom_tg_markup = types.InlineKeyboardMarkup(row_width=3)
prom_tg_markup.add(types.InlineKeyboardButton(text='Рассылки в Telegram', callback_data='prom_tg_1'))
prom_tg_markup.add(types.InlineKeyboardButton(text='Инвайт в группы', callback_data='prom_tg_2'))
prom_tg_markup.add(types.InlineKeyboardButton(text='Парсинг подписчиков', callback_data='prom_tg_3'))
prom_tg_markup.add(types.InlineKeyboardButton(text='PR компании', callback_data='prom_tg_4'))
prom_tg_markup.add(types.InlineKeyboardButton(text='Циклические публикации в чатах',
                                              callback_data='prom_tg_5'))
prom_tg_markup.add(types.InlineKeyboardButton(text='Посев нативных комментариев',
                                              callback_data='prom_tg_6'))
prom_tg_markup.add(types.InlineKeyboardButton(text='Комплексное продвижение', callback_data='prom_tg_7'))
prom_tg_markup.add(types.InlineKeyboardButton(text='<< Назад', callback_data='back_service'))

'''brief site markup'''
brief_site_markup = types.InlineKeyboardMarkup()
brief_site_markup.add(types.InlineKeyboardButton(text='Заполнить бриф', callback_data='brief_site_1'))
brief_site_markup.add(types.InlineKeyboardButton(text='Нужна помощь специалиста',
                                                 callback_data='brief_site_2'))

'''brief design markup'''
brief_design_markup = types.InlineKeyboardMarkup()
brief_design_markup.add(types.InlineKeyboardButton(text='Заполнить бриф', callback_data='brief_design_1'))
brief_design_markup.add(types.InlineKeyboardButton(text='Нужна помощь специалиста',
                                                   callback_data='brief_design_2'))

'''href to services'''
href_service_markup = types.InlineKeyboardMarkup()
href_service_markup.add(types.InlineKeyboardButton(text='Услуги', callback_data='back_service'))

'''invite from promotion telegram'''
prom_tg_invite_markup = types.InlineKeyboardMarkup()
prom_tg_invite_markup.add(types.InlineKeyboardButton(text='Отлично, хочу', callback_data='prom_tg_2_want'))
prom_tg_invite_markup.add(types.InlineKeyboardButton(text='Спасибо, я подумаю', callback_data='promotion_telegram'))

'''cycle and comments from promotion telegram'''
prom_tg_cycle_comments_markup = types.InlineKeyboardMarkup()
prom_tg_cycle_comments_markup.add(types.InlineKeyboardButton(text='Заказать услугу', callback_data='prom_tg_5_6_want'))
prom_tg_cycle_comments_markup.add(types.InlineKeyboardButton(text='Вернуться к списку услуг',
                                                             callback_data='promotion_telegram'))

'''newsletter from promotion telegram'''
prom_tg_newsletter_markup = types.InlineKeyboardMarkup()
prom_tg_newsletter_markup.add(types.InlineKeyboardButton(text='Да', callback_data='prom_tg_1_want'))
prom_tg_newsletter_markup.add(types.InlineKeyboardButton(text='Нет, нужна ваша помощь', callback_data='prom_tg_1_sup'))

'''number newsletter promotion telegram'''
prom_tg_newsletter_number_markup = types.InlineKeyboardMarkup()
prom_tg_newsletter_number_markup.add(types.InlineKeyboardButton(text='1000', callback_data='prom_tg_1_number_1'))
prom_tg_newsletter_number_markup.add(types.InlineKeyboardButton(text='2000', callback_data='prom_tg_1_number_2'))
prom_tg_newsletter_number_markup.add(types.InlineKeyboardButton(text='3000', callback_data='prom_tg_1_number_3'))
prom_tg_newsletter_number_markup.add(types.InlineKeyboardButton(text='5000', callback_data='prom_tg_1_number_4'))
prom_tg_newsletter_number_markup.add(types.InlineKeyboardButton(text='Более 10000', callback_data='prom_tg_1_number_5'))
prom_tg_newsletter_number_markup.add(types.InlineKeyboardButton(text='Указать количество',
                                                                callback_data='prom_tg_1_number_6'))

'''input number newsletter promotion telegram'''
prom_tg_newsletter_inp_number_markup = types.InlineKeyboardMarkup()
for i in range(10):
    prom_tg_newsletter_inp_number_markup.add(types.InlineKeyboardButton(text=f'{i}',
                                                                        callback_data=f'prom_tg_1_number_inp_{i}'))

'''input number last newsletter promotion telegram'''
prom_tg_newsletter_inp_last_number_markup = prom_tg_newsletter_inp_number_markup
prom_tg_newsletter_inp_last_number_markup.add(types.InlineKeyboardButton(text='Ввод окончен',
                                                                         callback_data='prom_tg_1_number_last'))

