import os
from pymongo import MongoClient

# passwd = None
# passwdfile = os.environ.get('OOPSY_DBPASS', None)
# if passwdfile:
#     passwd = open(passwdfile).readline().strip()

db = MongoClient(host=os.environ.get('OOPSY_DBHOST', 'localhost'),
                 port=int(os.environ.get('OOPSY_DBPORT', 27017))).oopsy
