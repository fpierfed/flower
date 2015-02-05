"""
Database read functionality. We are not writing to the DB here.
"""
from bson.objectid import ObjectId


class DB(object):
    """
    Abstract the DB-specific API
    """
    def __init__(self, db):
        self.db = db
        return

    def experiment_by_id(self, wid):
        return self.db.experiments.find_one({'_id': ObjectId(wid)})

    def experiments_by_timestamp(self):
        return self.db.experiments.find()
