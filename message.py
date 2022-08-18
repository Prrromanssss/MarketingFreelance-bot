import abc


class BaseMessages(abc.ABC):
    @abc.abstractmethod
    def start(self):
        raise NotImplemented


class Finish:
    def finish(self):
        text = 'Наш менеджер скоро свяжется с Вами'
        return text


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
        text = 'Пожалуй самый легкий способ заказать качественные услуги.\n' \
               '<small><small>Пользуясь сервисом вы соглашаетесь с обработкой ваших данных </small></small>'
        return text

    def support_start(self):
        text = 'Напишите Ваш вопрос'
        return text

    def support_finish(self):
        text = 'Наш менеджер скоро свяжется с Вами'
        return text

    def payment(self):
        text = 'Вы можете оплатить наши услуги с помощью банковских карт и кошельков Юмани, Qiwi'
        return text

    def success_pay(self):
        text = 'Оплата прошла успешно!'
        return text

    def unknown(self):
        text = 'Мы вас не понимаем'
        return text


class DevelopBots(BaseMessages, Finish):
    def __init__(self):
        self.flag_develop_bots = {}

    def start(self, name=None):
        text = 'Расскажите какие задачи должен выполнять чат-бот и какой функционал Вам интересен?\n' \
               'После заполнения нажмите кнопку «Далее»'
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
        text = 'Расскажите подробнее, о вашем товаре/услуге?\n' \
                'После заполнения нажмите кнопку «Далее»'

        return text

    def aim(self):
        text = 'Кто является вашей целевой аудиторией? Опишите портрет клиента\n' \
               'После заполнения нажмите кнопку «Далее»'
        return text

    def budget(self):
        text = 'Какой у Вас рекламный бюджет?'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с Вами в ближайшее время!'
        return text


class PromotionTelegram(BaseMessages, Finish):
    def __init__(self):
        self.flag_prom_tg = {}
        self.category = {}
        self.msg_for_delete = {}
        self.all_categories = {
                  '1': 'Рассылки в Telegram', '2': 'Парсинг подписчиков',
                  '3': 'Инвайт в группы', '4': 'PR компании',
                  '5': 'Циклические публикации в чатах', '6': 'Посев нативных комментариев',
                  '7': 'Комплексное продвижение'
                 }

    def start(self):
        text = 'Если вам нужно продвинуть ваши товары/услуги в telegram, то Вы обратились по адресу'
        return text

    def finish(self):
        text = 'Благодарим за заказ, мы свяжемся с вами в ближайшее время'
        return text


class ListPromotionTelegramNewsletter(BaseMessages):
    def start(self):
        text = 'У вас уже есть текст и креатив для рассылки?'
        return text

    def press_yes(self):
        text = 'Пришлите текст, креатив и ссылку на ваш канал/группу/сайт\n' \
                'После заполнения нажмите кнопку «Далее»'
        return text

    def success_payment(self):
        text = 'Спасибо за заказ.Наш менеджер свяжется с вами'
        return text

    def press_no(self):
        text = 'Наш менеджер скоро свяжется с Вами'
        return text


class ListPromotionTelegramInvite(BaseMessages, Finish):
    def start(self):
        text = 'С помощью данной услуги вы сможете собрать и подписать на свою группу подписчиков интересующих вас чатов'
        return text

    def press_yes(self):
        text = 'Отправьте ссылки на чаты, подписчики которых Вам интересны\n' \
               'После заполнения нажмите кнопку «Далее»'
        return text


class ListPromotionTelegramParsing(BaseMessages, Finish):
    def start(self):
        text = 'Пришлите ссылки на чаты/каналы подписчиков которых, вы хотите спарсить\n' \
               'После заполнения нажмите кнопку «Далее»'
        return text


class ListPromotionTelegramPR(BaseMessages, Finish):
    def start(self):
        text = 'С помощью нашего сервиса можно провести PR-компании в социальных сетях.\nОпишите ваши задачи\n' \
               'После заполнения нажмите кнопку «Далее»'
        return text


class ListPromotionTelegramCycle(BaseMessages, Finish):
    def start(self):
        text = 'С помощью нашего сервиса у вас есть возможность публиковать ваши сообщения в интересующих вас группах' \
               ' по заданному временному периоду, раз в 1час/2 часа и тд'
        return text


class ListPromotionTelegramComments(BaseMessages, Finish):
    def start(self):
        text = 'При заказе данной услуги, в нужных Вам чатах, размещаются сообщения содержащие нативную рекламу' \
               ' ваших товаров/услуг'
        return text


class ListPromotionTelegramComplex(BaseMessages, Finish):
    def start(self):
        text = 'complex'
        return text


class Sites(BaseMessages, Finish):
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


class Design(BaseMessages, Finish):
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


dev_bots = DevelopBots()
blog = Bloggers()
prom_tg = PromotionTelegram()
site = Sites()
design_obj = Design()
base = Basement()
admin = AdminUser()
reg_user = RegularUser()