class PwsEntry:
    def __init__(self, owner, login, enc, env_name):
        self._owner = owner
        self._login = login
        self._enc = enc
        self._env_name = env_name
        #self._created set by mongodb

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def set_owner(self, owner):
        self._owner = owner

    @property
    def login(self):
        return self._login

    @login.setter
    def set_login(self, login):
        self._login = login

    @property
    def enc(self):
        return self._enc

    @enc.setter
    def set_enc(self, enc):
        self._enc = enc

    @property
    def env_name(self):
        return self._env_name

    @env_name.setter
    def set_env(self, env_name):
        self._env_name = env_name

    def to_json(self):
        return {
            'owner': self._owner,
            'login': self._login,
            'enc': self._enc,
            'env_name': self._env_name
        }

    @staticmethod
    def to_pws(pws_dict):
        if pws_dict:
            return PwsEntry(pws_dict['owner'], pws_dict['login'], pws_dict['enc'], pws_dict['env_name'])
        return None
