from master.httpcontroller.action_controller import ActionController
from master.persistence.pws_store import PwsStore
from master.beans.pws_entries import PwsEntry
from master.util import create_json_status
from master.encryption.encrypt_bfish import MyBlowFish
from master.logger.file_logger import logger

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
        self.enc = None
        self.pws_store = PwsStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.env = self.get_request_parameter('env')
        self.user = self.get_request_parameter('user')
        self.password = self.get_request_parameter('password')
        if self.password:
            enc_key = self.env + self.user + self.get_current_login_user_id()
            self.enc = MyBlowFish(enc_key).encrypt(self.password)

    def get(self):
        current_login_id = self.get_current_login_user_id()
        pws_entry = self.pws_store.get_pws_by_login_env(current_login_id, self.user, self.env)
        password_entry = MyBlowFish(self.env + self.user + current_login_id).decrypt(pws_entry.enc)
        self.write_one_response(str_msg=create_json_status(True, password_entry.decode('utf-8')), all_cookies=[self._jsession_cookie])
        return None

    def add(self):
        current_login_id = self.get_current_login_user_id()
        self.pws_store.insert_new_pws(PwsEntry(current_login_id, self.user, self.enc, self.env))
        self.write_one_response(str_msg=create_json_status(True, 'User entry added.'), all_cookies=[self._jsession_cookie])
        return None

    def update(self):
        self.write_one_response(str_msg="OK update a pws.", all_cookies=[self._jsession_cookie])
        return None

    def delete(self):
        pass

    def other_action_mappings(self, action):
        pass