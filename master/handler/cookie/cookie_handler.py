from master.logger.file_logger import logger
from http import cookies


class CookieHandler:

    """
    Handler of HTTP cookies
    """
    def __init__(self):
        pass

    @staticmethod
    def get_cookie(request_handler, key):
        all_cookies = request_handler.headers.get_all('cookie', [])

        if all_cookies is not None:
            cookie_str = ', '.join(all_cookies)
            new_cookie = cookies.SimpleCookie()
            new_cookie.load(cookie_str)
            if key in new_cookie:
                logger().info(' found session id=' + new_cookie[key].value)
                new_cookie[key]['path'] = '/'
                return new_cookie[key]
            else:
                return None

        else:
            logger().warn(' No cookie found')
        return None

    def set_cookie(self, http_response, key, value):
        pass

    @staticmethod
    def create_new_cookie(key, value, path):
        new_cookie = cookies.SimpleCookie()
        new_cookie[key] = value
        new_cookie[key]['path'] = path
        return new_cookie

