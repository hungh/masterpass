from master.filters.abstract_filter import AbstractFilter
from master.sesscontroller.session_controller import SessionController
from master.logger.file_logger import logger
import re


class SessionFilter(AbstractFilter):
    """
    Except /login, any other request coming in requires a session
    """

    def __init__(self):
        pass

    def filter(self, request_handler):
        curr_path = request_handler.get_path()
        logger().info(' session filter path=' + curr_path)
        allow_paths = ['/login', '/index.html', '/']
        if curr_path in allow_paths \
                or re.match(r'/js/[\./\w-]+.js$', curr_path) \
                or re.match(r'[\w/]+.(?:html|jpg|css)$', curr_path):
            print(' by pass path=' + curr_path)
            return True, ""

        session_controller = SessionController()
        session_bean, is_new_jsession = session_controller.get_session(request_handler, False)
        if session_bean is not None:
            logger().info(" SessionFilter session_id=" + session_bean.session_id)
        else:
            logger().info(' No session found')
            return False, "No HTTP session"

        return True, ""
