import abc


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self):
        raise NotImplementedError


class Finish:
    def finish(self):
        text = 'Наш менеджер скоро свяжется с Вами'
        return text


class RegularUser(BaseMessages):
    def __init__(self):
        self.dialog_support = {}

    def start(self):
        text = (
            'Добро пожаловать!\n'
            'Давайте я помогу Вам в выборе услуги. '
            )
        return text

    def reg_user_close_dialog(self):
        text = 'Пользователь закрыл диалог'
        return text


class AdminUser(BaseMessages):
    def __init__(self):
        self.flag_for_password = {}
        self.flag_account = {}
        self.flag_for_newsletter = {}
        self.flag_for_write_user = {}
        self.flag_for_private_msg = {}
        self.user_to_send = {}
        self.msg_to_send = {}

    def start(self):
        text = (
            'Вы вошли в аккаунт администратора\n'
            'Вы можете создать рассылки для всех пользователей, присылая нам'
            ' медиафайлы, текст и другие сообщения.\n'
            'А также просмотреть всех ваших пользователей\n'
            )

        return text

    def write_password(self):
        text = 'Введите пароль, чтобы войти в качестве админа\n'
        return text

    def user_not_found(self):
        text = 'Данный пользователь не подписан на бота'
        return text

    def newsletter(self):
        text = (
            'Присылайте нам медиафайлы, документы и другие сообщения и они'
            ' будут отправлены всем пользователям\n'
            'Нажмите кнопку "Стоп", если хотите прекратить рассылку'
            )
        return text

    def send_private(self):
        text = (
            'Вы открыли диалог с пользователем\n'
            'Присылайте нам сообщения, они будут отправлены пользователю\n'
            'Если вы хотите закрыть диалог - нажмите «Закрыть диалог»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text

    def success_sending_private(self):
        text = 'Сообщения успешно отправлены'
        return text

    def write_username(self):
        text = 'Введите имя пользователя в формате "@пользователь"'
        return text

    def success_newsletter(self):
        text = 'Ваши сообщения успешно отправлены всем пользователям!'
        return text

    def password_false(self):
        text = 'Пароль введен неверно, попробуйте еще раз'
        return text

    def finish(self):
        text = 'Вы вернулись в аккаунт обычного пользователя'
        return text

    def admin_close_dialog(self):
        text = 'Менеджер закрыл диалог'
        return text


class Basement:
    def __init__(self):
        self.flag_support = {}
        self.category = {}

    def services(self):
        text = 'Что вас интересует? '
        return text

    def about(self):
        text = (
            'Пожалуй самый легкий способ заказать качественные услуги.\n'
            'Пользуясь сервисом вы соглашаетесь с обработкой ваших данных'
            )
        return text

    def support_start(self):
        text = 'Напишите Ваш вопрос'
        return text

    def support_finish(self):
        text = 'Наш менеджер скоро свяжется с Вами'
        return text

    def payment(self):
        text = (
            'Вы можете оплатить наши услуги с помощью банковских карт '
            'и кошельков Юмани, Qiwi'
            )
        return text

    def success_pay(self):
        text = 'Оплата прошла успешно!'
        return text

    def back_to_menu(self):
        text = 'Вернуться в главное меню'
        return text

    def unknown(self):
        text = 'Мы вас не понимаем'
        return text


class DevelopBots(BaseMessages, Finish):
    def __init__(self):
        self.flag_develop_bots = {}

    def start(self, name=None):
        text = (
            'Расскажите какие задачи должен выполнять чат-бот и '
            'какой функционал Вам интересен?\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text


class Bloggers(BaseMessages, Finish):
    def __init__(self):
        self.flag_for_bloggers = {}
        self.flag_detail_product = {}
        self.flag_aim = {}
        self.flag_budget = {}

    def start(self, name=None):
        text = 'Что Вы хотите рекламировать?'
        return text

    def detail_product(self):
        text = (
            'Расскажите подробнее о вашем товаре/услуге?\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )

        return text

    def aim(self):
        text = (
            'Кто является вашей целевой аудиторией? Опишите портрет клиента\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text

    def budget(self):
        text = 'Какой у Вас рекламный бюджет?'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с Вами в ближайшее время!'
        return text


class PromotionTelegram(BaseMessages, Finish):
    def __init__(self):
        self.flag_prom_tg, self.newsletter, self.number_newsletter = {}, {}, {}
        self.category, self.msg_for_delete = {}, {}
        self.all_categories = {
                  '1': 'Рассылки в Telegram',
                  '2': 'Парсинг подписчиков',
                  '3': 'Инвайт в группы',
                  '4': 'PR компании',
                  '5': 'Циклические публикации в чатах',
                  '6': 'Посев нативных комментариев',
                  '7': 'Комплексное продвижение'
                 }
        self.complex_href, self.complex_contact = {}, {}

    def start(self):
        text = 'Ниже представлены инструменты для продвижения в Telegram'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с вами в ближайшее время'
        return text


class ListPromotionTelegramNewsletter(BaseMessages, Finish):
    def start(self):
        text = 'У вас уже есть текст и креатив для рассылки?'
        return text

    def press_yes(self):
        text = (
            'Пришлите текст, креатив и ссылку на ваш канал/группу/сайт\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text

    def number(self):
        text = 'Какое количество сообщений Вам нужно отправить?'
        return text


class ListPromotionTelegramInvite(BaseMessages, Finish):
    def start(self):
        text = (
            'С помощью данной услуги вы сможете собрать '
            'и подписать на свою группу подписчиков интересующих вас чатов'
            )
        return text

    def press_yes(self):
        text = (
            'Отправьте ссылки на чаты, подписчики которых Вам интересны\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text


class ListPromotionTelegramParsing(BaseMessages, Finish):
    def start(self):
        text = (
            'Пришлите ссылки на чаты/каналы подписчиков которых, '
            'вы хотите спарсить\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text


class ListPromotionTelegramPR(BaseMessages, Finish):
    def start(self):
        text = (
            'С помощью нашего сервиса можно провести PR-компании '
            'в социальных сетях.\nОпишите ваши задачи\n'
            'После заполнения нажмите кнопку «Далее»\n'
            'Если кнопка не видна , нажмите 🎛'
            )
        return text


class ListPromotionTelegramCycle(BaseMessages, Finish):
    def start(self):
        text = (
            'С помощью нашего сервиса у вас есть возможность публиковать '
            'ваши сообщения в интересующих вас группах'
            ' по заданному временному периоду, раз в 1 час/2 часа и тд'
            )
        return text


class ListPromotionTelegramComments(BaseMessages, Finish):
    def start(self):
        text = (
            'При заказе данной услуги, в нужных Вам чатах, '
            'размещаются сообщения содержащие нативную рекламу'
            ' ваших товаров/услуг'
            )
        return text


class ListPromotionTelegramComplex(BaseMessages, Finish):
    def start(self):
        text = (
            'Заказывая <strong>комплексное продвижение в telegram</strong>,'
            ' вы получаете все инструменты от изучения вашей'
            ' ниши до разработки стратегии, построении воронки продаж и '
            'обработки заявок.\n\n'
            'Мы используем все доступные инструменты и алгоритмы продвижения '
            'для привлечения клиентов.\n\n '
            'Стоимость <strong>от 40000₽/месяц</strong>'
            )
        return text

    def href(self):
        text = 'Пришлите ссылку на ваш проект'
        return text

    def contact(self):
        text = 'Пришлите ваши контакты'
        return text


class Sites(BaseMessages, Finish):
    def __init__(self):
        self.flag_sites = {}
        self.flag_sup_brief = {}
        self.send_doc = {}

    def start(self, name=None):
        text = (
            'Вы уже знаете, какой сайт Вы хотите и '
            'готовы заполнить бриф для создания сайта'
            ' или нужна помощь специалиста?'
            )
        return text

    def fill_brief(self):
        text = 'Заполните бриф и пришлите его нам'
        return text

    def sup_brief(self):
        text = 'Укажите ваши контактные данные и удобное время для связи'
        return text


class Design(BaseMessages, Finish):
    def __init__(self):
        self.flag_design = {}
        self.flag_sup_brief = {}
        self.send_doc = {}

    def start(self, name=None):
        text = (
            'Вы уже знаете, какой дизайн Вы хотите и '
            'готовы заполнить бриф или нужна помощь специалиста?'
            )
        return text

    def fill_brief(self):
        text = 'Заполните бриф и пришлите его нам'
        return text

    def sup_brief(self):
        text = 'Укажите ваши контактные данные и удобное время для связи'
        return text


dev_bots = DevelopBots()
blog = Bloggers()
prom_tg = PromotionTelegram()
site = Sites()
design_obj = Design()
base = Basement()
admin = AdminUser()
reg_user = RegularUser()
