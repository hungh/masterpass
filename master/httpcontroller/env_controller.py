from master.httpcontroller.action_controller import ActionController
from master.persistence.env_store import EnvStore
from master.util import create_json_status

import json
import pymongo

ENV_ADD_MSG = 'Environment has been added successfully.'
ENV_DELETE_MSG = 'Environment has been removed successfully.'
ENV_DUP = 'This environment already exists in your account. Please pick another name.'


class EnvController(ActionController):
    def __init__(self, request_handler,  action):
        self.env = None
        self.env_store = EnvStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.env = self.get_request_parameter('env')

    def get(self):
        """
            Return all environments
        """
        all_env = self.env_store.get_all_env_by_owner(self.current_login_id)
        self.write_one_response(str_msg=json.dumps(all_env), all_cookies=[self._jsession_cookie])

    def add(self):
        try:
            self.env_store.insert_new_env_by_owner(self.env, self.current_login_id)
        except pymongo.errors.DuplicateKeyError:
            return create_json_status(False, ENV_DUP)
        self.write_one_response(str_msg=create_json_status(True, ENV_ADD_MSG), all_cookies=[self._jsession_cookie])

    def update(self):
        pass

    def delete(self):
        self.env_store.delete_env_by_owner(self.env, self.current_login_id)
        self.write_one_response(str_msg=create_json_status(True, ENV_DELETE_MSG), all_cookies=[self._jsession_cookie])

    def other_action_mappings(self, action):
        pass
