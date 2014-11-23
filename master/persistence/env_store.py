from master.boostrap.db_client import SingleDBClient
from master.persistence.pws_store import PwsStore
from pymongo import ASCENDING


class EnvStore:
    def __init__(self):
        self.client = SingleDBClient().get_client()
        self.db = self.client.env
        self.db.env_col.ensure_index([('owner', ASCENDING), ('name', ASCENDING)], unique=True)

    def get_all_env_by_owner(self, owner):
        all_env = []
        for env in self.db.env_col.find({'owner': owner}):
            all_env.append(env['name'])
        return all_env

    def insert_new_env_by_owner(self, env_string, owner):
        self.db.env_col.insert({'name': env_string, 'owner': owner})

    def delete_env_by_owner(self, env_name, owner):
        # WARNING: delete an ENV will erase all PWS entries of
        # the same ENV category
        self.db.env_col.remove({'owner': owner, 'name': env_name})
        PwsStore().delete_pws_by_owner_env(owner, env_name)
