from selenium.webdriver.support.ui import WebDriverWait


class Wait(WebDriverWait):

    def __init__(self, *args, **kwargs):
        super(Wait, self).__init__(None, *args, **kwargs)

    def until(self, method, message=''):
        return super(Wait, self).until(lambda _: method(), message)

    def until_not(self, method, message=''):
        return super(Wait, self).until_not(lambda _: method(), message)
