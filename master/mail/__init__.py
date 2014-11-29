from master.meta.singleton import Singleton

class AuthHolder(metaclass=Singleton):
    def __init__(self, smtp_password=''):
        self.smtp_password = smtp_password

    def get_smtp_pass(self):
        return self.smtp_password