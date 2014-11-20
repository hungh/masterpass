# root access to application
from master.boostrap.db_client import SingleDBClient
from master.beans.users import User
import bcrypt


def initialize():
    root_user = 'root'
    init_root_pw = 'password'
    user_collection = SingleDBClient().get_client().users.users_col
    existing_root = user_collection.find_one({"uid": root_user})

    if not existing_root or not existing_root['hash_pw']:
        hashed = bcrypt.hashpw(init_root_pw, bcrypt.gensalt())
        root = User(root_user, 'admin', 'lastadmin', hashed, 'True')
        user_collection.update({"uid": root_user}, {"$set": root.to_json()}, upsert=True)


