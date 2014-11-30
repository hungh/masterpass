from master.httpcontroller.base_controller import BaseHttpController
from master.persistence.users_store import UserStore
from master.util import get_optional_email
from master.sesscontroller.session_controller import SessionController
from master.volacontroller import VolatileController
from master.beans.nosession.reset_session import ResetPasswordBean
from master.mail import AuthHolder
from master.mail.send_mail import send_gmail
from master.logger.file_logger import logger

EMAIL_SENT_MSG_1 = 'An email has been set to your email to reset password.'

class AccountController(BaseHttpController):
    def __init__(self, request_handler, action):
        BaseHttpController.__init__(self, request_handler)
        self.user_id = None

    def control(self):
        logger().info("Account Controller")
        self.user_id = self.get_request_parameter('uid')

    def write_body(self):
        user = UserStore().get_user_by_id(self.user_id)
        if user:
            email = get_optional_email(user, True)
            logger().info('email to reset: {}'.format(email))
            # prepare volatile session
            hex = SessionController.gen_session_id()
            VolatileController().push_new_session(ResetPasswordBean(hex, user['uid']))
            msg = 'Please follow the link below to reset your password\nhttp://localhost:8009/' + hex
            send_gmail(email, msg, AuthHolder().get_smtp_pass())
        self.write_one_response(str_msg=EMAIL_SENT_MSG_1)



