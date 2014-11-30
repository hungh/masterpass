class MimeController:
    """
    MIME controller for HTTP web
    """
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_mime(self):
        url_path = self.request_handler.path.split('?')[0]
        mime_type = 'text/plain'

        if url_path.endswith('.html'):
            mime_type = 'text/html'
        elif url_path.endswith('.jpg'):
            mime_type = 'image/jpeg'
        elif url_path.endswith('.gif'):
            mime_type = 'image/gif'
        elif url_path.endswith('.js'):
            mime_type = 'application/javascript'
        elif url_path.endswith('.css'):
            mime_type = 'text/css'
        return mime_type
