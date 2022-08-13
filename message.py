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
    def services(self):
        text = 'Что вас интересует? '
        return text

    def about(self):
        text = ''
        return text

    def support(self):
        text = ''
        return text


class DevelopBots:
    ...


class Bloggers:
    ...


class PromotionTelegram:
    ...


class Sites:
    ...


class Design:
    ...


