import abc


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self):
        raise NotImplemented


class RegularUser(BaseMessages):
    def start(self):
        text = 'Добро пожаловать в электронного помощника компании ...\n' \
               'Давайте я помогу Вам в выборе услуги. '
        return text


class AdminUser(BaseMessages):
    def start(self):
        text = ''
        return text


class Basement:
    def __init__(self):
        self.flag_support = {}
        self.category = {}

    def services(self):
        text = 'Что вас интересует? '
        return text

    def about(self):
        text = 'О нас'
        return text

    def support_start(self):
        text = 'Напишите Ваш вопрос'
        return text

    def support_finish(self):
        text = 'Мы уже работаем над решением проблемы, ожидайте ответа.'
        return text


class DevelopBots(BaseMessages):
    def __init__(self):
        self.flag_develop_bots = {}

    def start(self):
        text = 'Расскажите какие задачи должен выполнять чат-бот и какой функционал Вам интересен'
        return text

    def finish(self):
        text = 'Благодарим за сообщение, мы свяжемся с Вами в ближайшее время!'
        return text


class Bloggers(BaseMessages):
    def __init__(self):
        self.flag_bloggers = {}

    def start(self):
        text = 'Что Вы хотите рекламировать?'
        return text


class PromotionTelegram(BaseMessages):
    def __init__(self):
        self.flag_prom_tg = {}
        self.category = {}

    def start(self):
        text = 'Если вам нужно продвинуть ваши товары/услуги в telegram, то Вы обратились по адресу'
        return text

    def prom_tg_markup(self):
        text = 'Опишите ваши задачи, пришлите ссылку на ваш канал/группу или сайт и оставьте ваши контакты'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с вами в ближайшее время'
        return text


class Sites(BaseMessages):
    def __init__(self):
        self.flag_sites = {}
        self.flag_sup_brief = {}

    def start(self):
        text = 'Вы уже знаете, какой сайт Вы хотите и готовы заполнить бриф для создания сайта' \
               ' или нужна помощь специалиста?'
        return text

    def fill_brief(self):
        text = 'Заполните бриф и пришлите его нам'
        return text

    def sup_brief(self):
        text = 'Укажите ваши контактные данные и удобное время для связи'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с вами в ближайшее время'
        return text


class Design(BaseMessages):
    def __init__(self):
        self.flag_design = {}
        self.flag_sup_brief = {}

    def start(self):
        text = 'Вы уже знаете, какой дизайн Вы хотите и готовы заполнить бриф или нужна помощь специалиста?'
        return text

    def fill_brief(self):
        text = 'Заполните бриф и пришлите его нам'
        return text

    def sup_brief(self):
        text = 'Укажите ваши контактные данные и удобное время для связи'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с вами в ближайшее время'
        return text


dev_bots = DevelopBots()
blog = Bloggers()
prom_tg = PromotionTelegram()
site = Sites()
design_obj = Design()
base = Basement()
