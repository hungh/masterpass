from master.handler.cookie.cookie_handler import CookieHandler
from master.beans.session.session_bean import SessionBean
from master.meta.singleton import Singleton

from master.consts import SESSION_TIMEOUT, SESSION_USER_ID

from uuid import uuid4


class SessionController(metaclass=Singleton):

    def __init__(self):
        self.all_session_beans = dict()

    def invalidate_session_by_login(self, owner):
        for session_id in self.all_session_beans.keys():
            session_bean = self.all_session_beans[session_id]
            if not session_bean:
                continue
            if owner == session_bean.get_attribute(SESSION_USER_ID):
                self.invalidate_session(session_id)

    def invalidate_session(self, session_id):
        try:
            print('[DEBUG] invalidating session id=' + session_id)
            del self.all_session_beans[session_id]
        except KeyError:
            pass

    def get_all_session(self):
        return self.all_session_beans

    def get_session(self, request_handler, will_create_new):
        """
        :param request_handler: master.handler.CustomHTTPHandler
        :param will_create_new: true to create a new session if there is no existing session
        :return: SessionBean, Boolean (created new or not)
        """
        jsession_cookie = CookieHandler.get_cookie(request_handler, 'JSESSIONID')
        ret_session_bean = None
        is_new_jsession = False

        if jsession_cookie is None:
            if will_create_new is True:
                sid = uuid4().hex
                is_new_jsession = True
                ret_session_bean = SessionBean(sid)
                self.all_session_beans[sid] = ret_session_bean
        else:
            is_cookie_found = True
            is_session_found = True
            existing_jsession_id = None
            try:
                existing_jsession_id = jsession_cookie.value
                if existing_jsession_id in self.all_session_beans:
                    ret_session_bean = self.all_session_beans[existing_jsession_id]

                if ret_session_bean is None:
                    is_session_found = False

            except KeyError:
                print('No Cookie found')
                is_cookie_found = False

            if is_cookie_found is False or is_session_found is False:
                if will_create_new is True:
                    # re-use JSESSIONID
                    if existing_jsession_id is None:
                        existing_jsession_id = uuid4().hex
                        is_new_jsession = True

                    ret_session_bean = SessionBean(existing_jsession_id)

                    self.all_session_beans[existing_jsession_id] = ret_session_bean

        return ret_session_bean, is_new_jsession

    @staticmethod
    def get_jsession_cookie(request_handler):
        """
        Get SimpleCookie JSESSIONID
        :param request_handler master.handler.CustomHTTPHandler
        :return: http.cookies.SimpleCookie
        """
        return CookieHandler.get_cookie(request_handler, 'JSESSIONID')

    @staticmethod
    def get_session_timeout():
        """
        Get session time out in milliseconds
        :return:
        """
        return SESSION_TIMEOUT

    @staticmethod
    def gen_session_id():
        return uuid4().hex





