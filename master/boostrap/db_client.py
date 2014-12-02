from master.meta.singleton import Singleton
from master.beans.nosession import AuthHolder
from master.consts import DB_SERVER_PORT
from pymongo import MongoClient


class SingleDBClient(metaclass=Singleton):
    def __init__(self):
        print('[INFO] Creating MongoDB client connection...')
        self._client = MongoClient(AuthHolder().get_mongod_server(), DB_SERVER_PORT)

    def get_client(self):
        return self._client

