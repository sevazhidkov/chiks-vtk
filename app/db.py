import os
from pymongo import MongoClient

client = MongoClient(os.environ['MONGO_URL']).get_default_database()
db = client.chicks_vtk
