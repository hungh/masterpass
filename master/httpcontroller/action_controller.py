from master.httpcontroller.base_controller import BaseHttpController
from master.sesscontroller.session_controller import SessionController
from master.logger.file_logger import logger
from master.consts import ADD_ACTION, UPDATE_ACTION, GET_ACTION
from abc import ABCMeta, abstractmethod


class ActionController(BaseHttpController):
    __metaclass__ = ABCMeta

    def __init__(self, request_handler,  action):

        if action is None:
            raise Exception('Unable to collect action based on action None')

        self._request_handler = request_handler
        self._action = action
        self._jsession_cookie = None
        self._data = {}
        BaseHttpController.__init__(self, request_handler)

    def control(self):
        pass

    def write_body(self):
        logger().info('user action =' + self._action)
        self._jsession_cookie = SessionController.get_jsession_cookie(self.request_handler)
        #< err is string >#
        err = None
        if self._action == ADD_ACTION:
            err = self.add_user()
        elif self._action == GET_ACTION:
            err = self.get_user()
        elif self._action == UPDATE_ACTION:
            err = self.update_user(self._data)
        if err:
            self.write_one_response(str_msg=err, all_cookies=[self._jsession_cookie])

    @abstractmethod
    def get_user(self):
        """
        :return: error string or None
        """
        pass

    @abstractmethod
    def add_user(self):
        """
        :return: error string or None
        """
        pass

    @abstractmethod
    def update_user(self, user):
        """
        :return: error string or None
        """
        pass


