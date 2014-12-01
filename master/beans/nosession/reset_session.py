class ResetPasswordBean:
    def __init__(self, sess_id, uid):
        self.sess_id = sess_id
        self.uid = uid

    @property
    def session_id(self):
        return self.sess_id

    @session_id.setter
    def set_session_id(self, sess_id):
        self.sess_id = sess_id

    @property
    def user_id(self):
        return self.uid

    @user_id.setter
    def set_user_id(self, uid):
        self.uid = uid
