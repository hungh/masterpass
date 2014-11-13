from master.httpcontroller.action_controller import ActionController


class PwsController(ActionController):
    def __init__(self, request_handler,  action):
        """
        Constructor (1)
        :param request_handler: http.server.SimpleHTTPRequestHandler
        :param action: string get action (add, get and update) pws
        /pws/add?  /pws/get?uid=jin u/pws/update?uid=jin
        """
        ActionController.__init__(self, request_handler, action)

    def control(self):
        pass

    def get_user(self):
        self.write_one_response(str_msg="OK get a pws.", all_cookies=[self._jsession_cookie])
        return None

    def add_user(self):
        self.write_one_response(str_msg="OK add a pws.", all_cookies=[self._jsession_cookie])
        return None

    def update_user(self, user):
        self.write_one_response(str_msg="OK update a pws.", all_cookies=[self._jsession_cookie])
        return None
