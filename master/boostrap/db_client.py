from master.meta.singleton import Singleton
from master.consts import DB_SERVER_PORT
from pymongo import MongoClient


class SingleDBClient(metaclass=Singleton):
    def __init__(self):
        print('Creating MongoDB Client ')
        self._client = MongoClient('localhost', DB_SERVER_PORT)

    def get_client(self):
        return self._client

