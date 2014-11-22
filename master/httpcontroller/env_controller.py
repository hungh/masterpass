from master.httpcontroller.action_controller import ActionController
from master.persistence.env_store import EnvStore
from master.util import create_json_status
import json
import pymongo


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
        all_env = self.env_store.get_all_env()
        self.write_one_response(str_msg=json.dumps(all_env), all_cookies=[self._jsession_cookie])

    def add(self):
        try:
            self.env_store.insert_new_env(self.env)
        except pymongo.errors.DuplicateKeyError:
            return create_json_status(False, 'Duplicate environment.')
        self.write_one_response(str_msg=create_json_status(True, 'Environment added.'), all_cookies=[self._jsession_cookie])

    def update(self):
        pass

    def delete(self):
        pass

    def other_action_mappings(self, action):
        pass
