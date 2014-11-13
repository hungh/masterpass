from master.httpcontroller.base_controller import BaseHttpController
from master.sesscontroller.session_controller import SessionController


class LogoutController(BaseHttpController):

    def __init__(self, request_handler):
        BaseHttpController.__init__(self, request_handler)

    def control(self):
        new_http_session, is_new_jsession = SessionController().get_session(self.request_handler, False)
        if new_http_session is not None:
            SessionController().invalidate_session(new_http_session.session_id)

    def write_body(self):
        jsession_cookie = SessionController.get_jsession_cookie(self.request_handler)
        if jsession_cookie is not None:
            jsession_cookie['expires'] = 'Thu, 01-Jan-70 00:00:01 GMT;'
        self.write_one_response(str_msg="Successfully logged out.", all_cookies=[jsession_cookie])
