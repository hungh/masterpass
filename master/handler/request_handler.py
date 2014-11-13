from master.httpcontroller.controllers_maps import getHttpController
from master.logger.file_logger import logger
from master.filters.filter_chain import filter_chain
from master.blocker.ip_blocker import IPBlocker
from urllib.parse import urlparse
import http.server

NOT_AUTHORIZED = 'Not authorize to use application.'


class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP handler for web application
    """
    def __init__(self, request, client_address, server):
        self.no_op = False
        if IPBlocker.should_block(client_address[0]):
            # no operation
            self.no_op = True
            return
        super(CustomHTTPHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        if self.no_op:
            logger().info('access is being blocked')
            return
        status, msg = filter_chain(self)
        if status is True:
            http_controller = getHttpController(self.path, self)
            http_controller.process()
        else:
            self.filter_fail(NOT_AUTHORIZED)

    def do_POST(self):
        if self.no_op:
            logger().info('access is being blocked')
            return
        status, msg = filter_chain(self)
        if status is True:
            http_controller = getHttpController(self.path, self)
            http_controller.process()
        else:
            self.filter_fail(NOT_AUTHORIZED)

    def get_path(self):
        return urlparse(self.path).path

    def filter_fail(self, err_msg):
        encoded_err_msg = err_msg.encode('utf-8')
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(encoded_err_msg))
        self.end_headers()
        self.wfile.write(encoded_err_msg)
