from master.meta.singleton import Singleton
from master.consts import DEFAULT_PORT

class AuthHolder(metaclass=Singleton):
    def __init__(self, smtp_password='', web_server_port=DEFAULT_PORT):
        self.smtp_password = smtp_password
        self.web_server_port = web_server_port

    def get_smtp_pass(self):
        return self.smtp_password

    def get_web_server_port(self):
        return self.web_server_port