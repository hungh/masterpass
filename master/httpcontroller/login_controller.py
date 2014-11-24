from master.httpcontroller.base_controller import BaseHttpController
from master.handler.cookie.cookie_handler import CookieHandler
from master.sesscontroller.session_controller import SessionController
from master.persistence.users_store import UserStore
from master.consts import SESSION_USER_ID
from master.logger.file_logger import logger
from master.util import create_json_status
import bcrypt


class LoginController(BaseHttpController):

    def __init__(self, request_handler):
        BaseHttpController.__init__(self, request_handler)
        self.login = None
        self.password = None

    def control(self):
        logger().info("LoginController")
        self.login = self.get_request_parameter('login')
        self.password = self.get_request_parameter('password')
        logger().info('Login=' + self.login + ';password=' + self.password)

    def write_body(self):
        if LoginController.is_valid_user(self.login, self.password):
            # create a new session
            new_http_session, is_new_jsession = SessionController().get_session(self.request_handler,
                                                                                will_create_new=True)
            # save password into http session as a key for other encryption and decryption
            new_http_session.set_attribute(SESSION_USER_ID, self.login)

            jsession_cookie = None
            if new_http_session is not None:
                logger().info('user is authenticated.')
                if is_new_jsession is True:
                    jsession_cookie = CookieHandler.create_new_cookie('JSESSIONID', new_http_session.session_id, '/')
                self.write_one_response(str_msg=create_json_status(True, '/work.html'), all_cookies=[jsession_cookie])

        else:
            self.write_one_response(str_msg=create_json_status(False, 'Either login name or password is incorrect.'))

    @staticmethod
    def is_valid_user(user_id, password_str):
        if user_id is None or password_str is None:
            return False
        try:
            user_conn = UserStore()
            hashpw_str = user_conn.get_hashpw(user_id)
        finally:
            user_conn.close()
        if hashpw_str is None:
            return False
        return bcrypt.checkpw(password_str, hashpw_str)