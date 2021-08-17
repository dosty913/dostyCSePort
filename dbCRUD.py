#CRUD Code for dashboard
#Daniel Ostrin

import os
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import pprint

# Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
connectMongo = "mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority"
# Create the database for our example (we will use the same database throughout the tutorial
client = pymongo.MongoClient(connectMongo)
# set our actual database to db
mydb = client.mongodb_eBids
mycol = mydb.eBids

class BidSystem(object):
    """ CRUD operations for items collection in MongoDB """
     
    def __init__(self,):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
        self.client = pymongo.MongoClient(connectMongo)
        # set our actual database to mycol
        self.database = self.client['mongodb_eBids']

    # Create method to implement the C in CRUD
    def create(self, data):
        if data is not None:
            self.database.eBids.insert(data) # data should be dictionary
            return True
        else:
            print('Nothing to save, because data parameter is empty')
            return False

    # Read method to implement the R in CRUD
    def read(self, data):
        if data is not None:
            return self.database.eBids.find(data,{"_id":False})
        else:
            print('Nothing to read, because data parameter is empty')
            return False
    
    # Update method to implement the U in CRUD
    def update(self, data, change):
        if data is not None:
            return self.database.eBids.update(data,{ "$set": change}) # data and change are dictionaries
        else:
            print('Nothing to update, because data parameter is empty')
            return False
            
    # Delete method to implement the D in CRUD
    def delete(self, data):
        if data is not None:
            return self.database.eBids.delete_one(data) # data is dictionary 
        else: 
            print('Nothing to delete, because data parameter is empty')
            return False

    
