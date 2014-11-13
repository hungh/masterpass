from pymongo.son_manipulator import SONManipulator

from master.beans.users import User
from master.beans.pws_entries import PwsEntry


def transform_incoming_main(son, collection, object_type, encode_custom):
        """
            from memory to storage(mongodb)
            :param object_type: class type (User or PWsEntry)
            :param encode_custom: function to encode python object to dict
        """
        for (key, value) in son.items():
            if isinstance(value, object_type):
                son[key] = encode_custom(value)
            elif isinstance(value, dict):
                son[key] = transform_incoming_main(value, collection, object_type, encode_custom)
        return son


def transform_outgoing_main(son, collection, custom_str, decode_custom):
        """
            from storage (mongodb) to python memory
            :param custom_str: string type of user
            :param decode_custom: function to decode dict into python object
        """
        for(key, value) in son.items():
            if isinstance(value, dict):
                if "_type" in value and value["_type"] == custom_str:
                    son[key] = decode_custom(value)
                else:
                    son[key] = transform_outgoing_main(value, collection, custom_str, decode_custom)
        return son


class UserTransform(SONManipulator):
    """
    convert User into mongodb-compatible insert data
    """
    def transform_incoming(self, son, collection):
        return transform_incoming_main(son, collection, User, UserTransform.encode_custom)

    def transform_outgoing(self, son, collection):
        return transform_outgoing_main(son, collection, "user", UserTransform.decode_custom)

    @staticmethod
    def encode_custom(user):
        return {"_type": "user", "uid": user.uid, "first": user.first, "last":
                user.last, "hash_pw": user.hash_pw, "admin": user.admin}

    @staticmethod
    def decode_custom(user_doc):
        assert user_doc["_type"] == "user"
        return User(user_doc["uid"], user_doc["first"], user_doc["last"], user_doc["hash_pw"], user_doc["admin"])


class PwsEntryTransform(SONManipulator):
    def transform_incoming(self, son, collection):
        return transform_incoming_main(son, collection, PwsEntry, PwsEntryTransform.encode_custom)

    def transform_outgoing(self, son, collection):
        return transform_outgoing_main(son, collection, "pwsentry", PwsEntryTransform.decode_custom)

    @staticmethod
    def encode_custom(pws_entry):
        return {"_type": "pwsentry", "login": pws_entry.login, "enc": pws_entry.enc, "env_name": pws_entry.env_name}

    @staticmethod
    def decode_custom(pws_doc):
        assert pws_doc["_type"] == "pwsentry"
        return PwsEntry(pws_doc["login"], pws_doc["enc"], pws_doc["env_name"])
