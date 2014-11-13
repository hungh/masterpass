# root access to application
from master.boostrap.db_client import SingleDBClient
from master.beans.users import User
import bcrypt


def initialize():
    user_collection = SingleDBClient().get_client().users.users_col
    # uid, first, last, hash_pw, admin)
    root_password = 'password'
    hashed = bcrypt.hashpw(root_password, bcrypt.gensalt())
    root = User('root', 'root', 'root', hashed, 'True')
    user_collection.update({"uid": root.uid}, {"$set": root.to_json()}, upsert=True)


