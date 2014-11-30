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

    def get_session(self, hex):
        return self.all_volatile_sessions[hex]

    def invalidate(self, hex):
        try:
            del self.all_volatile_sessions[hex]
        except KeyError:
            logger().error('Trying to invalidate invalid session:' + hex)
