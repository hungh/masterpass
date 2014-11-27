from master.boostrap.db_client import SingleDBClient
from master.persistence.env_store import EnvStore
from master.util import get_optional_email
from master.logger.file_logger import logger
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
            return one_record['hash_pw']
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

    def get_all_users(self):
        all_users = []
        for user in self.db.users_col.find():
            all_users.append({'id': user['uid'], 'first': user['first'], 'last': user['last'], 'email': get_optional_email(user, True)})

        return all_users

    def get_user_by_id(self, uid):
        return self.db.users_col.find_one({'uid': uid})

    def update_user_by_id(self, user):
        email = get_optional_email(user)
        self.db.users_col.update({"uid": user.uid}, {"$set": {"first": user.first, "last": user.last, "email": email}})

    def update_user_with_hash(self, uid, hash_pw):
        self.db.users_col.update({"uid": uid}, {"$set": {"hash_pw": hash_pw}})

    def delete_user_by_id(self, user_uid):
        self.db.users_col.remove({"uid": user_uid})
        all_env_by_owner = EnvStore().get_all_env_by_owner(user_uid)
        if all_env_by_owner:
            for env in all_env_by_owner:
                EnvStore().delete_env_by_owner(env, user_uid)

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
