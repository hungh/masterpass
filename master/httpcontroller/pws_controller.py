from master.httpcontroller.action_controller import ActionController
from master.persistence.pws_store import PwsStore


class PwsController(ActionController):
    def __init__(self, request_handler,  action):
        """
        Constructor (1)
        :param request_handler: http.server.SimpleHTTPRequestHandler
        :param action: string get action (add, get and update) pws
        /pws/add?  /pws/get?uid=jin u/pws/update?uid=jin
        """
        self.env = None
        self.user = None
        self.password = None
        self.pws_store = PwsStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.env = self.get_request_parameter('env')
        self.user = self.get_request_parameter('user')
        self.password = self.get_request_parameter('password')

    def get(self):
        self.write_one_response(str_msg="OK get a pws.", all_cookies=[self._jsession_cookie])
        return None

    def add(self):
        self.write_one_response(str_msg="OK add a pws.", all_cookies=[self._jsession_cookie])
        return None

    def update(self):
        self.write_one_response(str_msg="OK update a pws.", all_cookies=[self._jsession_cookie])
        return None

    def delete(self):
        pass

    def other_action_mappings(self, action):
        pass