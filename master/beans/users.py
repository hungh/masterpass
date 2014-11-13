class User:
    """
    users who login to the web application
    """
    def __init__(self, uid, first, last, hash_pw, admin):
        self._uid = uid
        self._first = first
        self._last = last
        self._hash_pw = hash_pw
        self._admin = admin

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def set_uid(self, uid):
        self._uid = uid

    @property
    def first(self):
        return self._first

    @first.setter
    def set_first(self, first):
        self._first = first

    @property
    def last(self):
        return self._last

    @last.setter
    def set_last(self, last):
        self._last = last

    @property
    def hash_pw(self):
        return self._hash_pw

    @hash_pw.setter
    def set_hash(self, hash_pw):
        self._hash_pw = hash_pw

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def set_admin(self, admin):
        """
        :param admin: string of 'True' or 'False'
        """
        self._admin = admin

    def to_json(self):
        """
        Looks like SONManipulator does not support 'manipulate' for update
        This is called only for update
        """
        return {
            'uid': self._uid,
            'first': self._first,
            'last': self._last,
            'hash_pw': self._hash_pw,
            'admin': self._admin
        }

    @staticmethod
    def to_user(one_user):
        return User(one_user['uid'], one_user['first'], one_user['last'], one_user['hash_pw'], one_user['admin'])



