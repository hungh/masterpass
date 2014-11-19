from master.boostrap.db_client import SingleDBClient


class EnvStore:
    def __init__(self):
        self.client = SingleDBClient().get_client()
        self.db = self.client.env

    def get_all_env(self):
        all_env = []
        for env in self.db.env_col.find():
            all_env.append(env['_id'])
        return all_env

    def insert_new_env(self, env_string):
        self.db.env_col.insert({'_id': env_string})
