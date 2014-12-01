from master.meta.singleton import Singleton


class AuthHolder(metaclass=Singleton):
    def __init__(self, web_server_port=None,
                 web_host_name=None,
                 google_mail=None,
                 google_mail_pass=None,
                 smtp_server=None,
                 mongod_server=None):
        self.web_server_port = web_server_port
        self.web_host_name = web_host_name
        self.google_mail = google_mail
        self.google_mail_pass = google_mail_pass
        self.smtp_server = smtp_server
        self.mongod_server = mongod_server

    def get_google_mail_pass(self):
        return self.smtp_password

    def get_web_server_port(self):
        return self.web_server_port

    def get_web_host_name(self):
        return self.web_host_name

    def get_google_mail(self):
        return self.google_mail

    def get_google_mail_pass(self):
        return self.google_mail_pass

    def get_smtp_server(self):
        return self.smtp_server

    def get_mongod_server(self):
        return self.mongod_server

    def __str__(self):
        return 'Listening on:' + str(self.web_server_port) + "\n" + \
                'Web server name:' + self.web_host_name + "\n" +\
               'Gmail:' + self.google_mail + "\n" +\
                'MongoDB:' + self.mongod_server + "\n" +\
               'SMTP Server:' + self.smtp_server + "\n"