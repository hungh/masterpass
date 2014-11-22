from master.httpcontroller.action_controller import ActionController
from master.httpcontroller.login_controller import LoginController
from master.persistence.pws_store import PwsStore
from master.beans.pws_entries import PwsEntry
from master.util import create_json_status, get_clear_text, gen_enc_string
from master.consts import GET_PWS_OWNER


class PwsController(ActionController):
    def __init__(self, request_handler,  action):
        """
                Constructor
                :param request_handler: http.server.SimpleHTTPRequestHandler
                :param action: string get action (add, get and update) pws
        """
        self.env = None
        self.user = None
        self.password = None
        self.master_password = None
        self.enc = None
        self.pws_store = PwsStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.env = self.get_request_parameter('env')
        self.user = self.get_request_parameter('user')
        self.password = self.get_request_parameter('password')
        self.master_password = self.get_request_parameter('masterPassword')
        if self.password:
            if LoginController.is_valid_user(self.current_login_id, self.master_password):
                self.enc = gen_enc_string(self.master_password, self.password)

    def get(self):
        if self.user and self.env:
            pws_entry = self.pws_store.get_pws_by_login_env(self.current_login_id, self.user, self.env)
            clear_password = get_clear_text(self.master_password, pws_entry.enc)
            self.write_one_response(str_msg=create_json_status(True, clear_password), all_cookies=[self._jsession_cookie])

    def add(self):
        if not self.enc:
            self.write_one_response(str_msg=create_json_status(False, 'Invalid password'))
        elif self.user and self.env:
            self.pws_store.insert_new_pws(PwsEntry(self.current_login_id, self.user, self.enc, self.env))
            self.write_one_response(str_msg=create_json_status(True, 'User entry added.'), all_cookies=[self._jsession_cookie])

    def update(self):
        if not self.enc:
            self.write_one_response(str_msg=create_json_status(False, 'Invalid password'))
        elif self.env and self.user and self.password:
            self.pws_store.update_pws_password(self.current_login_id, self.user, self.env, self.enc)
            self.write_one_response(str_msg=create_json_status(True, 'Entry updated.'), all_cookies=[self._jsession_cookie])

    def delete(self):
        if self.user:
            self.pws_store.delete_pws_entry(self.current_login_id, self.user)
            self.write_one_response(str_msg=create_json_status(True, 'Entry deleted.'), all_cookies=[self._jsession_cookie])

    def get_pws_by_owner(self):
        all_pws_owner = self.pws_store.get_pws_by_owner(self.current_login_id)
        self.write_one_response(str_msg=create_json_status(True, all_pws_owner), all_cookies=[self._jsession_cookie])

    def other_action_mappings(self, action):
        if action == GET_PWS_OWNER:
            self.get_pws_by_owner()


