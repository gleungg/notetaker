from pymongo import MongoClient
from dotenv import load_dotenv
import os
import models

load_dotenv()

ATLAS_URI = os.environ.get("ATLAS_URI")
DB_NAME = "Notes"

'''
Read: Find luckerdog by name
Write: Add luckerdog instance to database
'''
class Database:
    def __init__(self): 
        self.client = self.startupDbClient()

    def registerUser(self, record: models.Luckerdog):
        db = self.connectDb("Luckerdogs")
        print(db.find_one({"luckerdog": record["luckerdog"]}))
        if db.find_one({"luckerdog": record["luckerdog"]}):
            raise Exception("Luckerdog already exists")
        db.insert_one(record)
        
    def addNote(self, record: models.Record):
        try:
            db = self.connectDb("Records")
            db.insert_one(record)
        except Exception as e:
            print("Error adding note: ", e)

    def getNotes(self, name):
        db = self.connectDb("Records")
        return db.find({"name": name})

    def connectDb(self, collection):
        return self.client["Notes"][collection]

    def startupDbClient(self):
        client = MongoClient(ATLAS_URI)
        return client
        
    def shutdownDb(self):
        self.client.close()

if __name__ == "__main__":
    db = Database()
