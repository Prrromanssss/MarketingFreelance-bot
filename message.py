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
    def __init__(self):
        self.flag_for_password = {}
        self.flag_account = {}
        self.flag_for_newsletter = {}

    def start(self):
        text = f'Вы вошли в аккаунт администратора\n' \
               f'Вы можете создать рассылки для всех пользователей, присылая нам медиафайлы, текст и другие сообщения.\n' \
               f'А также просмотреть всех ваших пользователей\n' \

        return text

    def write_password(self):
        text = 'Введите пароль, чтобы войти в качестве админа\n' \
               'Пароль: 0000'
        return text

    def newsletter(self):
        text = 'Присылайе нам медиафайлы, документы и другие сообщения и они будут отправлены всем пользователям\n' \
               f'Нажмите кнопку "Стоп", если хотите прекратить рассылку'
        return text

    def success_newsletter(self):
        text = 'Ваши сообщения успешно отправлены всем пользователям!'
        return text

    def password_false(self):
        text = f'Пароль введен неверно, попробуйте еще раз'
        return text

    def finish(self):
        text = 'Вы вернулись в аккаунт обычного пользователя'
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

    def payment(self):
        text = 'Описание возможностей оплаты услуг'
        return text

    def success_pay(self):
        text = 'Оплата прошла успешно!'
        return text

    def unknown(self):
        text = 'Мы вас не понимаем'
        return text


class DevelopBots(BaseMessages):
    def __init__(self):
        self.flag_develop_bots = {}

    def start(self, name=None):
        text = 'Расскажите какие задачи должен выполнять чат-бот и какой функционал Вам интересен?\n' \
               'Как закончите свое описание нажмите кнопку "Всё"'
        return text

    def finish(self):
        text = 'Благодарим за сообщение, мы свяжемся с Вами в ближайшее время!'
        return text


class Bloggers(BaseMessages):
    def __init__(self):
        self.flag_for_bloggers = {}
        self.flag_network = {}
        self.flag_aim = {}
        self.flag_budget = {}

    def start(self, name=None):
        text = 'Что Вы хотите рекламировать?'
        return text

    def network(self):
        text = 'В какой социальной сети?'
        return text

    def aim(self):
        text = 'Кто является вашей целевой аудиторией? Опишите портрет клиента'
        return text

    def budget(self):
        text = 'Какой у Вас рекламный бюджет?'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с Вами в ближайшее время!'
        return text


class PromotionTelegram(BaseMessages):
    def __init__(self):
        self.flag_prom_tg = {}
        self.category = {}

    def start(self, name=None):
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
        self.send_doc = {}

    def start(self, name=None):
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
        self.send_doc = {}

    def start(self, name=None):
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
admin = AdminUser()