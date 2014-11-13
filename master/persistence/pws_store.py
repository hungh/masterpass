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

    def update_pws(self,  pws_object):
        self.db.pws_col.update({'owner': pws_object.owner, 'login': pws_object.login, 'env_name': pws_object.env_name}, {'$set': pws_object.to_json()})

    def close(self):
        self.client.close()

    def drop_pws_col(self):
        self.client.drop_database('pws')

"""
s = PwsStore()
#s.drop_pws_col()
e = PwsEntry('h2', 'hung', 'AHDA&DASD*AS*D', 'dev4')
s.insert_new_pws(e)
print(s.get_pws_by_login_env(e.owner, e.login, e.env_name).login)

e.set_enc = 'NEW_ENC'
s.update_pws(e)

print(s.get_pws_by_login_env(e.owner, e.login, e.env_name).enc)
s.close()
"""


