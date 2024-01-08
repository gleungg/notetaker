"""Database module"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

import models

load_dotenv()

ATLAS_URI = os.environ.get("ATLAS_URI")
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
        print(db.find_one({"luckerdog": record["luckerdog"]}))
        if db.find_one({"luckerdog": record["luckerdog"]}):
            raise Exception("Luckerdog already exists")
        db.insert_one(record)

    def addNote(self, record: models.Record):
        """Add a lucky event to the database"""
        try:
            db = self.connectDb("Records")
            db.insert_one(record)
        except Exception as e:
            print("Error adding note: ", e)

    def getNotes(self, name):
        """Get all notes for a given luckerdog"""
        db = self.connectDb("Records")
        return db.find({"name": name})

    def connectDb(self, collection):
        """Connect to the database and return the collection"""
        return self.client["Notes"][collection]

    def startupDbClient(self):
        """Connect to the database"""
        client = MongoClient(ATLAS_URI)
        return client

    def shutdownDb(self):
        """Close the database connection"""
        self.client.close()


if __name__ == "__main__":
    db = Database()
