from master.httpcontroller.action_controller import ActionController
from master.httpcontroller.login_controller import LoginController
from master.sesscontroller.session_controller import SessionController

from master.persistence.users_store import UserStore
from master.persistence.pws_store import PwsStore

from master.beans.users import User
from master.consts import CURRENT_USER_ACTION, CHANGE_PW_ACTION, ALL_ACTIVE_SESSION, SESSION_USER_ID

import bcrypt
import json
import math

USER_ADD_MSG = 'User has been added successfully.'
USER_UPDATE_MSG = 'User has been updated successfully.'
USER_DELETE_MSG = 'User has been removed successfully.'
USER_INVALID_PASS = 'Please enter a correct password.'
USER_CHANGE_PASS = 'Your password has been changed successfully.'
ROOT_NO_DELETE = 'admin user cannot be deleted.'


class UserController(ActionController):
    def __init__(self, request_handler,  action):
        """
        Constructor
        :param request_handler: http.server.SimpleHTTPRequestHandler
        :param action: string get action (add, get and update) user
        """
        self.id = None
        self.first = None
        self.last = None
        self.password = None
        self.new_password = None
        self.email = None
        self.user_store = UserStore()
        ActionController.__init__(self, request_handler, action)

    def control(self):
        self.id = self.get_request_parameter('id')
        self.first = self.get_request_parameter('first')
        self.last = self.get_request_parameter('last')
        self.email = self.get_request_parameter('email')
        self.password = self.get_request_parameter('password')
        self.new_password = self.get_request_parameter('new_password')

    def change_password(self, current_login_id):
        if self.new_password:
            self.user_store.update_user_with_hash(current_login_id, bcrypt.hashpw(self.new_password, bcrypt.gensalt()))
            # updating all pws entries
            PwsStore().change_all_pws_enc(self.current_login_id, self.password, self.new_password)

    def get_user_sessions(self):
        if not self.is_root():
            return None
        all_sessions = SessionController().get_all_session()
        ret_session = []

        for session_id in all_sessions.keys():
            session_bean = all_sessions[session_id]
            if session_bean:
                trimmed_index = math.trunc(len(session_id)/3)
                ret_session.append({'user': session_bean.get_attribute(SESSION_USER_ID),
                                    'session': session_id[0: trimmed_index]})
        return ret_session

    def get(self):
        """
        Get all users
        """
        if not self.is_root():
            return None
        all_user = self.user_store.get_all_users()
        self.write_one_response(str_msg=json.dumps(all_user))

    def add(self):
        if not self.is_root():
            return None
        if self.id and self.password:
            hash_pw = bcrypt.hashpw(self.password, bcrypt.gensalt())

            if self.email:
                new_user = User(self.id, self.first, self.last, hash_pw, False, self.email)
            else:
                new_user = User(self.id, self.first, self.last, hash_pw, False)
            self.user_store.insert_new_user(new_user)
            self.write_one_response(str_msg=USER_ADD_MSG)

    def update(self):
        if not self.is_root():
            return None
        if self.id:
            self.user_store.update_user_by_id(User(self.id, self.first, self.last, None, False, self.email))
            self.write_one_response(str_msg=USER_UPDATE_MSG)

    def delete(self):
        if not self.is_root():
            return None
        # you can not delete root himself
        if self.id == 'root':
            return ROOT_NO_DELETE

        self.user_store.delete_user_by_id(self.id)
        SessionController().invalidate_session_by_login(self.id)
        self.write_one_response(str_msg=USER_DELETE_MSG)

    def other_action_mappings(self, action):
        if action == CURRENT_USER_ACTION:
            self.write_one_response(str_msg=str(self.current_login_id))

        elif action == ALL_ACTIVE_SESSION:
            all_session = self.get_user_sessions()
            self.write_one_response(str_msg=json.dumps(all_session))

        elif action == CHANGE_PW_ACTION:
            if not LoginController.is_valid_user(self.current_login_id, self.password):
                return USER_INVALID_PASS
            self.change_password(self.current_login_id)
            self.write_one_response(str_msg=USER_CHANGE_PASS)

    def is_root(self):
        """
        Return True if user is root
        :return: boolean
        """
        return 'root' == self.current_login_id
