from master.consts import SESSION_TIMEOUT
from time import time


class SessionBean:
    """
    Represents session information per user
    """
    def __init__(self, sess_id):
        """
        constructor
        :param sess_id: session id
        :return:
        """
        self.sess_id = sess_id
        self.sess_attributes = {}
        self.timestamp = time()

    @property
    def session_id(self):
        return self.sess_id

    @session_id.setter
    def session_id(self, sess_id):
        self.sess_id = sess_id

    def set_attribute(self, attr_key, attr_value):
        """
        Set an attribute to session
        :param attr_key: string
        :param attr_value: object
        :return:
        """
        self.error_if_session_valid()
        self.sess_attributes[attr_key] = attr_value

    def get_attribute(self, attr_key):
        """
        Get an attribute from session
        :param attr_key: string key attribute
        :return: object
        """
        self.error_if_session_valid()
        return self.sess_attributes.get(key=attr_key)

    def re_use_session(self, new_sess_id):
        """
        Re-use this session bean object
        :param new_sess_id: string a new JSESSIONID
        """
        self.sess_id = new_sess_id
        self.sess_attributes.clear()
        self.timestamp = time()

    def error_if_session_valid(self):
        """
        Throw ValueError exception if session expires
        """
        if self.timestamp + SESSION_TIMEOUT <= time():
            raise ValueError('Session timed out.')
