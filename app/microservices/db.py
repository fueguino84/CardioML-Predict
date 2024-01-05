from flask import current_app, g
from pymongo import MongoClient

def get_db():
    if 'db' not in g:
        print("registramos una conexión")

        uri = "mongodb+srv://appuser:fT1vi2lbedB5Z7Nl@rolagooglecluster0.yojjtkq.mongodb.net/?retryWrites=true&w=majority"
        g.db = MongoClient(uri)

    return g.db
