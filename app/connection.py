from pymongo import MongoClient


client = MongoClient("mongodb://mongoadmin:mongoadmin@localhost:27017/")
db = client["db_tech"]