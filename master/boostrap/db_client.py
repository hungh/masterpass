from master.meta.singleton import Singleton
from master.consts import DB_SERVER_PORT, DB_SERVER_HOST
from pymongo import MongoClient


class SingleDBClient(metaclass=Singleton):
    def __init__(self):
        print('Creating MongoDB Client ')
        self._client = MongoClient(DB_SERVER_HOST, DB_SERVER_PORT)

    def get_client(self):
        return self._client

