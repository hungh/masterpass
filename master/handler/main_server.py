from master.handler.request_handler import CustomHTTPHandler
from master.boostrap.db_client import SingleDBClient
import socketserver


class MainHttpServer:

    @staticmethod
    def start(port):
        httpd = None
        try:
            httpd = socketserver.TCPServer(('', port), CustomHTTPHandler)

            print("[INFO] Serving at port", port)

            httpd.serve_forever()
        except KeyboardInterrupt:
            print("[WARN] ^C received. shutting down server.")
            httpd.server_close()
            SingleDBClient().get_client().close()
        finally:
            # close up data base connection
            if httpd is not None:
                httpd.server_close()
