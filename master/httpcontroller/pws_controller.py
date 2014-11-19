from master.httpcontroller.action_controller import ActionController
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
        self.enc = None
        self.pws_store = PwsStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.env = self.get_request_parameter('env')
        self.user = self.get_request_parameter('user')
        self.password = self.get_request_parameter('password')
        if self.password:
            self.enc = gen_enc_string(self.env, self.user, self.password, self.current_login_id)

    def get(self):
        pws_entry = self.pws_store.get_pws_by_login_env(self.current_login_id, self.user, self.env)
        clear_password = get_clear_text(self.env, self.user, pws_entry, self.current_login_id)
        self.write_one_response(str_msg=create_json_status(True, clear_password), all_cookies=[self._jsession_cookie])

    def add(self):
        self.pws_store.insert_new_pws(PwsEntry(self.current_login_id, self.user, self.enc, self.env))
        self.write_one_response(str_msg=create_json_status(True, 'User entry added.'), all_cookies=[self._jsession_cookie])

    def update(self):
        new_enc = gen_enc_string(self.env, self.user, self.password, self.current_login_id)
        self.pws_store.update_pws_password(self.current_login_id, self.user, self.env, new_enc)
        self.write_one_response(str_msg=create_json_status(True, 'Entry updated.'), all_cookies=[self._jsession_cookie])

    def delete(self):
        pass

    def get_pws_by_owner(self):
        all_pws_owner = self.pws_store.get_pws_by_owner(self.current_login_id)
        self.write_one_response(str_msg=create_json_status(True, all_pws_owner), all_cookies=[self._jsession_cookie])

    def other_action_mappings(self, action):
        if action == GET_PWS_OWNER:
            self.get_pws_by_owner()


