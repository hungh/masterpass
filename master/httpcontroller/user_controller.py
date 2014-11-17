from master.httpcontroller.action_controller import ActionController
from master.persistence.users_store import UserStore
from master.beans.users import User
import bcrypt
import json


class UserController(ActionController):
    def __init__(self, request_handler,  action):
        """
        Constructor (1)
        :param request_handler: http.server.SimpleHTTPRequestHandler
        :param action: string get action (add, get and update) user
        /user/add?  /user/get?uid=jin u/user/update?uid=jin
        """
        self.id = None
        self.first = None
        self.last = None
        self.password = None
        self.user_store = UserStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.id = self.get_request_parameter('id')
        self.first = self.get_request_parameter('first')
        self.last = self.get_request_parameter('last')
        self.password = self.get_request_parameter('password')

    def get_user(self):
        """
        Get all users
        """
        all_user = self.user_store.get_all_users()
        self.write_one_response(str_msg=json.dumps(all_user), all_cookies=[self._jsession_cookie])

    def add_user(self):
        hashpw = bcrypt.hashpw(self.password, bcrypt.gensalt())
        self.user_store.insert_new_user(User(self.id, self.first, self.last, hashpw, False))
        self.write_one_response(str_msg="Successfully add a user." + self.id + ";" + self.last, all_cookies=[self._jsession_cookie])

    def update_user(self, user):
        self.user_store.update_user_by_id(User(self.id, self.first, self.last, None, False))
        self.write_one_response(str_msg="Successfully update a user.", all_cookies=[self._jsession_cookie])
