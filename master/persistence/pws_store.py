from master.boostrap.db_client import SingleDBClient
from master.beans.pws_entries import PwsEntry
from pymongo import ASCENDING


class PwsStore:
    def __init__(self):
        self.client = SingleDBClient().get_client()
        self.db = self.client.pws
        self.db.pws_col.ensure_index([('owner', ASCENDING), ('login', ASCENDING)], unique=True)

    def insert_new_pws(self, pws_object):
        self.db.pws_col.insert(pws_object.to_json())

    def get_pws_by_login_env(self, owner, login, env_name):
        return PwsEntry.to_pws(self.db.pws_col.find_one({'owner': owner, 'login': login, 'env_name': env_name}))

    def get_pws_by_owner(self, owner):
        all_pws = []
        for pws_entry in self.db.pws_col.find({'owner': owner}):
            all_pws.append({'env_name': pws_entry['env_name'], 'login': pws_entry['login']})
        return all_pws

    def update_pws_password(self,  owner, login, env, enc):
        self.db.pws_col.update({'owner': owner, 'login': login, 'env_name': env}, {'$set': {'enc': enc}})

    def close(self):
        self.client.close()

    def drop_pws_col(self):
        self.client.drop_database('pws')


