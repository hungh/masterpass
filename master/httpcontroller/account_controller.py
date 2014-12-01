from master.beans.nosession import AuthHolder
from master.httpcontroller.base_controller import BaseHttpController
from master.persistence.users_store import UserStore
from master.util import get_optional_email
from master.sesscontroller.session_controller import SessionController
from master.httpcontroller.redirect_controller import RedirectController
from master.volacontroller import VolatileController
from master.beans.nosession.reset_session import ResetPasswordBean
from master.consts import REDIRECT_ACTION, UPDATE_ACTION, RESET_ACTION
from master.mail.send_mail import send_mail
from master.logger.file_logger import logger
import bcrypt

EMAIL_SENT_MSG_1 = 'An email has been set to your email to reset password.'


class AccountController(BaseHttpController):
    def __init__(self, request_handler, action):
        BaseHttpController.__init__(self, request_handler)
        self.user_id = None
        self.action = action

    def control(self):
        logger().info("Account Controller")
        self.user_id = self.get_request_parameter('uid')
        self.reset_id = self.get_request_parameter('sid')
        self.new_password = self.get_request_parameter('password')

    def write_body(self):
        if self.action == UPDATE_ACTION and self.reset_id and self.new_password:
            self.reset_password()
        elif self.action == REDIRECT_ACTION and self.reset_id:
        # redirect to reset password page
            RedirectController(self.request_handler, '/reset.html?sid=' + self.reset_id).write_body()
        elif self.action == RESET_ACTION and self.user_id:
            self.send_email()

    def reset_password(self):
        volatile_controller = VolatileController()
        if volatile_controller.is_valid_id(self.reset_id):
            user_id = volatile_controller.get_session(self.reset_id).user_id
            logger().info('User ID from vola session=' + user_id)
            new_hash = bcrypt.hashpw(self.new_password, bcrypt.gensalt())
            UserStore().update_user_with_hash(user_id, new_hash)
            VolatileController().invalidate(self.reset_id)
            self.write_one_response(str_msg="Your password has been reset")
        else:
            self.write_one_response(str_msg="Invalid credentials for a password reset link")

    def send_email(self):
        user = UserStore().get_user_by_id(self.user_id)
        if user:
            email = get_optional_email(user, True)
            logger().info('email to reset: {}'.format(email))
            if email:
                # prepare volatile session
                sid = SessionController.gen_session_id()
                VolatileController().push_new_session(ResetPasswordBean(sid, user['uid']))
                web_server_port = AuthHolder().get_web_server_port()
                msg = 'Please click on the link below to reset your password\nhttp://{}:{}/account/{}?sid={}'.\
                    format(AuthHolder().get_web_host_name(), web_server_port, REDIRECT_ACTION, sid)
                send_mail(email, msg)
        self.write_one_response(str_msg=EMAIL_SENT_MSG_1)



