from master.logger.file_logger import logger
from master.boostrap.db_client import SingleDBClient
from pymongo import ASCENDING


class UserStore:
    """
    IMPORTANT: mongod (server) needs to be running to use this class
    Example:
    user_t = UserStore()
    print(user_t.get_hashpw(1)) # 1: admin's id
    user_t.close()
    """

    def __init__(self):
        self.client = SingleDBClient().get_client()
        self.db = self.client.users
        self.db.users_col.ensure_index('uid', ASCENDING, unique=True)
        # self.db.add_son_manipulator(UserTransform())

    def get_hashpw(self, user_id):
        """
        get hashed bcrypt password
        :param user_id: integer (for now)
        :return: string hash pw
        """
        one_record = self.db.users_col.find_one({"uid": user_id})
        if one_record is not None:
            _hashpw = one_record['hash_pw']
            logger().info('hashpw-user[=' + _hashpw)
            return _hashpw
        else:
            logger().warn('Unable to find record of user_id:' + user_id)
        return None

    def insert_new_user(self, user):
        """
        Insert a new record into DB store
        :param user: json object {id:, first:, last:, hashpw:}
        :return: post id
        """
        return self.db.users_col.insert(user.to_json())

    def get_user_by_id(self, uid):
        return self.db.users_col.find_one({'uid': uid})

    def update_user_by_id(self, user):
        self.db.users_col.update({"uid": user.uid}, {"$set": user.to_json()})

    def get_total_users(self):
        return self.db.users_col.count()

    def close(self):
        self.client.close()

    def drop_users(self):
        self.client.drop_database("users")

    def get_user_collection(self):
        """
        Only used by bootstrap
        :return: mongodb collection
        """
        return self.db.users_col

