from master.httpcontroller.base_controller import BaseHttpController
from master.sesscontroller.session_controller import SessionController
from master.logger.file_logger import logger
from master.consts import ADD_ACTION, UPDATE_ACTION, GET_ACTION, DELETE_ACTION
from abc import ABCMeta, abstractmethod


class ActionController(BaseHttpController):
    __metaclass__ = ABCMeta

    def __init__(self, request_handler,  action):

        if action is None:
            raise Exception('Unable to collect action based on action None')

        self._request_handler = request_handler
        self._action = action
        self._jsession_cookie = None
        BaseHttpController.__init__(self, request_handler)

    def control(self):
        pass

    def write_body(self):
        logger().info('user action =' + self._action)
        self._jsession_cookie = SessionController.get_jsession_cookie(self.request_handler)
        #< err is string >#
        if self._action == ADD_ACTION:
            err = self.add()
        elif self._action == GET_ACTION:
            err = self.get()
        elif self._action == UPDATE_ACTION:
            err = self.update()
        elif self._action == DELETE_ACTION:
            err = self.delete()
        else:
            err = self.other_action_mappings(self._action)
        if err:
            self.write_one_response(str_msg=err, all_cookies=[self._jsession_cookie])

    @abstractmethod
    def get(self):
        """
        :return: error string or None
        """
        pass

    @abstractmethod
    def add(self):
        """
        :return: error string or None
        """
        pass

    @abstractmethod
    def update(self):
        """
        :return: error string or None
        """
        pass

    @abstractmethod
    def delete(self):
        """
        Delete user
        """
        pass

    @abstractmethod
    def other_action_mappings(self, action):
        """
        Return string if error, None otherwise
        :param action: string HTTP query
        :return:
        """
        pass

