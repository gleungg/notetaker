"""Database module"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

import models

load_dotenv()

ATLAS_URI = os.environ.get("ATLAS_URI")
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "Notes"


class Database:
    '''
    Read: Find luckerdog by name
    Write: Add luckerdog instance to database
    '''

    def __init__(self):
        self.client = self.startupDbClient()

    def registerUser(self, record: models.Luckerdog):
        """Add a luckerdog to the database"""
        db = self.connectDb("Luckerdogs")
        if db.find_one({"name": record['name']}):
            return str(f"{record['name']} is already registered.")
        db.insert_one(record)

    def addNote(self, record: models.Record):
        """Add a lucky event to the database"""
        try:
            db = self.connectDb("Records")
            if db.find_one({"name": record['name']}):
                db.insert_one(record)
                return str(f"Noted that {record['name']} is a luckerdog. \"{' '.join(record['event'])}\"")
            else:
                return str(f"{record['name']} is not registered. Are you sure this guy is a luckerdog?")
        except Exception as e:
            print("Error adding note: ", e)

    def getNotes(self, name):
        """Get all notes for a given luckerdog"""
        db = self.connectDb("Records")
        return db.find({"name": name})

    def connectDb(self, collection):
        """Connect to the database and return the collection"""
        print("Trying to connect")
        return self.client["Notes"][collection]

    def startupDbClient(self):
        """Connect to the database"""
        client = MongoClient(ATLAS_URI or MONGODB_URI)
        return client

    def shutdownDb(self):
        """Close the database connection"""
        self.client.close()


if __name__ == "__main__":
    db = Database()
