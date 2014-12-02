from master.filters.abstract_filter import AbstractFilter
from master.sesscontroller.session_controller import SessionController
from master.logger.file_logger import logger
from master.consts import ALLOWED_PATHS, NOT_AUTHORIZED, SESSION_EXPIRED
import re


class SessionFilter(AbstractFilter):
    """
    Except ALLOWED_PATHS, any other request coming in requires a session
    """

    def __init__(self):
        pass

    def filter(self, request_handler):
        curr_path = request_handler.get_path()
        logger().info(' session filter path=' + curr_path)
        if curr_path in ALLOWED_PATHS \
                or re.match(r'/js/[\./\w-]+.js$', curr_path) \
                or re.match(r'[\w/]+.(?:html|jpg|png|css)$', curr_path):
          
            return True, ""

        session_controller = SessionController()
        session_bean, is_new_jsession = session_controller.get_session(request_handler, False)
        if session_bean:
            if not session_bean.is_session_valid():
                # invalidate expired session
                session_controller.invalidate_session(session_bean.session_id)
                return False, SESSION_EXPIRED
            logger().info(" SessionFilter session_id=" + session_bean.session_id)
        else:
            logger().info(' No session found or timed out')
            return False, NOT_AUTHORIZED

        return True, ""
