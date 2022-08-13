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

    def services(self):
        text = 'Что вас интересует? '
        return text


class AdminUser(BaseMessages):
    def start(self):
        text = ''
        return text
