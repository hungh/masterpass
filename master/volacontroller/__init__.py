from master.meta.singleton import Singleton
from master.logger.file_logger import logger


class VolatileController(metaclass=Singleton):
    def __init__(self):
        self.all_volatile_sessions = dict()

    def push_new_session(self, reset_password_session):
        """

        :param hex: string uuid.hex
        :param reset_password_session: master.beans.nosession.reset_session.ResetPasswordBean
         """
        self.all_volatile_sessions[reset_password_session.session_id] = reset_password_session

    def get_session(self, reset_id):
        return self.all_volatile_sessions[reset_id]

    def invalidate(self, reset_id):
        try:
            del self.all_volatile_sessions[reset_id]
        except KeyError:
            logger().error('Trying to invalidate invalid session:' + reset_id)

    def is_valid_id(self, reset_id):
        try:
            self.all_volatile_sessions[reset_id]
        except KeyError:
            return False
        return True

