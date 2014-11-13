from master.httpcontroller.base_controller import BaseHttpController


class RedirectController(BaseHttpController):
    """
    Redirect response to another url
    """
    def __init__(self, request_handler, location):
        BaseHttpController.__init__(self, request_handler)
        self.location = location

    def control(self):
        pass

    def write_body(self):
        self.write_redirect(self.location)


