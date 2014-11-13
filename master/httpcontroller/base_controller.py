from master.mimecontroller.mime_controller import MimeController
from master.sesscontroller.session_controller import SessionController
from master.logger.file_logger import logger
from abc import ABCMeta, abstractmethod
from urllib.parse import urlparse, parse_qs
import cgi
import os


class BaseHttpController():
    __metaclass__ = ABCMeta

    def __init__(self, request_handler):
        """
        :param request_handler master.handler.CustomHTTPHandler (http.server.SimpleHTTPRequestHandler)
        """
        self.request_handler = request_handler
        self.mime_controller = MimeController(request_handler)
        self.form = None

    @staticmethod
    def get_resource():
        return os.getcwd() + '/../resources'

    def process(self):
        """
        Process HTTP request
        @private
        """
        if self.get_request_method() == 'POST':
            self.prepare_incoming_data_POST()
        elif self.get_request_method() == 'GET':
            self.prepare_incoming_data_GET()

        self.control()
        self.write_body()

    @abstractmethod
    def control(self):
        pass

    @abstractmethod
    def write_body(self):
        mime_type = self.mime_controller.get_mime()
        # not recognize file type
        f = None
        if mime_type is None:
            return

        file_full_path = BaseHttpController.get_resource() + self.request_handler.path
        try:
            f = open(file_full_path)
        except FileNotFoundError:
            self.write_one_response(response_code=404, str_msg='404 ERROR: File not found.')
            return
        finally:
            if f:
                f.close()

        self.write_one_response(response_code=200, content_type=mime_type, file_full_path=file_full_path)

    def prepare_incoming_data_GET(self):
        if self.form is None:
            self.form = {}

        url_object = urlparse(self.request_handler.path)
        qs = parse_qs(url_object.query)
        for k,v in qs.items():
            self.form[k] = v[0]

    def prepare_incoming_data_POST(self):
        logger().info("in POST")
        if self.get_request_method() != 'POST':
            return

        self.form = cgi.FieldStorage(
            fp=self.request_handler.rfile,
            headers=self.request_handler.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.request_handler.headers['Content-Type'], })

    def start_write_response(self, content_len, response_code=200, content_type="text/html", all_cookies=None):
        """
        Return wfile (HTTP Request handler's writer) to write out to http response
        :param content_len: required value (in bytes)
        :param all_cookies array of Morsel cookies
        :return: wfile HTTP request handler writer
        """
        self.request_handler.send_response(response_code )
        self.request_handler.send_header('Content-type', content_type)
        self.request_handler.send_header('Content-Length', content_len)
        jsession_cookie = SessionController.get_jsession_cookie(self.request_handler)
        if all_cookies is not None:
            to_written_cookies = all_cookies
        else:
            to_written_cookies = [jsession_cookie]

        for each_cookie in to_written_cookies:
            if each_cookie is not None:
                kv_pairs = str(each_cookie).split(':')
                if len(kv_pairs) > 1:
                    self.request_handler.send_header(kv_pairs[0], kv_pairs[1])

        self.request_handler.end_headers()
        return self.request_handler.wfile

    def write_fileto_response(self, wfile, f):
        buffer_size = 1024
        try:
            byte = f.read(buffer_size)
            while True:
                wfile.write(byte)
                byte = f.read(buffer_size)
                if not byte:
                    break
        finally:
            f.close()

    def get_request_method(self):
        """
        used by self.control()
        :return:
        """
        return self.request_handler.command

    def get_request_parameter(self, param_name):
        """
        used by self.control()
        :param param_name:
        :return:
        """
        request_method = self.get_request_method()
        logger().info('Request_method=' + request_method)
        try:
            if request_method == 'GET':
                return self.form[param_name]
            elif request_method == 'POST':
                return self.form[param_name].value

        except KeyError:
            return None

        return self.form[param_name].value

    def write_one_response(self, response_code=200, content_type="text/html", str_msg=None,
                           file_full_path=None, all_cookies=None):
        """
        str_msg is always get written first.
        :param str_msg: string
        :param file: file
        :return:
        """
        if str_msg is not None:
            # get size of data
            encoded_msg = str_msg.encode('utf-8')
            logger().info("Writing message=" + str_msg)
            data_len = len(encoded_msg)
            wfile = self.start_write_response(data_len, response_code, content_type, all_cookies)
            wfile.write(encoded_msg)
        elif file_full_path is not None:
            data_len = os.path.getsize(file_full_path)
            logger().info("Writing a file=" + file_full_path)
            wfile = self.start_write_response(data_len, response_code, content_type, all_cookies)
            self.write_fileto_response(wfile, open(file_full_path, 'rb'))
        else:
            raise Exception('Unable to send empty data in response')

    def write_redirect(self, location):
        self.request_handler.send_response(302)
        self.request_handler.send_header('Location', location)
        kv_pairs = str(SessionController.get_jsession_cookie(self.request_handler)).split(':')
        if len(kv_pairs) > 1:
            self.request_handler.send_header(kv_pairs[0], kv_pairs[1])
        self.request_handler.end_headers()
