from master.httpcontroller.action_controller import ActionController
from master.persistence.users_store import UserStore
from master.sesscontroller.session_controller import SessionController
from master.httpcontroller.login_controller import LoginController
from master.consts import SESSION_USER_ID, CURRENT_USER_ACTION, CHANGE_PW_ACTION
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
        self.new_password = None
        self.user_store = UserStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.id = self.get_request_parameter('id')
        self.first = self.get_request_parameter('first')
        self.last = self.get_request_parameter('last')
        self.password = self.get_request_parameter('password')
        self.new_password = self.get_request_parameter('new_password')

    def get_current_login_user_id(self):
        """
        Return the current login id in HTTP session
        """
        session_bean, was_created_new = SessionController().get_session(self.request_handler, will_create_new=False)
        return session_bean.get_attribute(SESSION_USER_ID)

    def change_password(self, current_login_id):
        self.user_store.update_user_with_hash(current_login_id, bcrypt.hashpw(self.new_password, bcrypt.gensalt()))

    def get(self):
        """
        Get all users
        """
        if not self.is_root():
            return None
        all_user = self.user_store.get_all_users()
        self.write_one_response(str_msg=json.dumps(all_user), all_cookies=[self._jsession_cookie])

    def add(self):
        if not self.is_root():
            return None
        hash_pw = bcrypt.hashpw(self.password, bcrypt.gensalt())
        self.user_store.insert_new_user(User(self.id, self.first, self.last, hash_pw, False))
        self.write_one_response(str_msg="Successfully add a user." + self.id + ";" + self.last, all_cookies=[self._jsession_cookie])

    def update(self):
        if not self.is_root():
            return None
        self.user_store.update_user_by_id(User(self.id, self.first, self.last, None, False))
        self.write_one_response(str_msg="Successfully update a user.", all_cookies=[self._jsession_cookie])

    def delete(self):
        if not self.is_root():
            return None
        # you can not delete root himself
        if self.id == 'root':
            return 'Error:root user cannot be deleted.'
        self.user_store.delete_user_by_id(self.id)
        self.write_one_response(str_msg="Successfully delete user " + self.id, all_cookies=[self._jsession_cookie])

    def other_action_mappings(self, action):
        current_login_id = self.get_current_login_user_id()

        if action == CURRENT_USER_ACTION:
            self.write_one_response(str_msg=str(current_login_id), all_cookies=[self._jsession_cookie])
        elif action == CHANGE_PW_ACTION:
            if not LoginController.is_valid_user(current_login_id, self.password):
                return "Incorrect password provided"
            self.change_password(current_login_id)
            self.write_one_response(str_msg="Your password was changed.", all_cookies=[self._jsession_cookie])

    def is_root(self):
        """
        Return True if user is root
        :return: boolean
        """
        return 'root' == self.get_current_login_user_id()
