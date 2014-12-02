from pymongo.errors import DuplicateKeyError
from master.boostrap.db_client import SingleDBClient
from master.beans.pws_entries import PwsEntry
from master.encryption.encrypt_bfish import MyBlowFish

from pymongo import ASCENDING


class PwsStore:
    def __init__(self):
        self.client = SingleDBClient().get_client()
        self.db = self.client.pws
        self.db.pws_col.ensure_index([('owner', ASCENDING), ('login', ASCENDING)], unique=True)

    def insert_new_pws(self, pws_object):
        try:
            self.db.pws_col.insert(pws_object.to_json())
        except DuplicateKeyError:
            return "Duplicate entry found"
        return None

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

    def delete_pws_entry(self, owner, pws_login):
        self.db.pws_col.remove({'owner': owner, 'login': pws_login})

    def delete_pws_by_owner(self, owner):
        self.db.pws_col.remove({'owner': owner})

    def delete_pws_by_owner_env(self, owner, env_name):
        self.db.pws_col.remove({'owner': owner, 'env_name': env_name})

    def change_all_pws_enc(self, owner, old_master_password, master_password):
        """
        :param owner: string id of the owner
        :param old_master_password: string old master password
        :param master_password: string new master password
        """
        updating_record = []
        for pws_entry in self.db.pws_col.find({'owner': owner}):
            each_clear_text = MyBlowFish(old_master_password).decrypt(pws_entry['enc'])
            new_enc = MyBlowFish(master_password).encrypt(each_clear_text.decode('utf-8'))
            updating_record.append({'login': pws_entry['login'],
                                    'env_name': pws_entry['env_name'], 'enc': new_enc})

            # updating records back
        if len(updating_record) > 0:
            for new_pws_entry in updating_record:
                self.update_pws_password(owner, new_pws_entry['login'], new_pws_entry['env_name'], new_pws_entry['enc'])




