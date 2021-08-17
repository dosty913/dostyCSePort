#CRUD Code for dashboard
#Daniel Ostrin

import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import pprint

class BidSystem(object):
    """ CRUD operations for items collection in MongoDB """
     
    def __init__(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
        self.client = pymongo.MongoClient("mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority")
        # set our actual database to mycol
        self.database = self.client['mongodb_eBids']

    # Create method to add new items to the Bid database.
    def create(self, data):
        if data is not None:
            data_create = self.database.items.insert(data)  # data should be dictionary
            return data_create
        else:
            raise Exception("Nothing to save, because data parameter is incorrectly formatted")

    # Read method to find one or all items within the Bid database.
    def read(self,data):
        if data is not None:    
            data_read = self.database.items.find_one(data,)
            return data_read
        else:
            raise Exception("Nothing to read because data parameter is incorrectly formatted")
    def readAll(self, data):    
        data_read = self.database.items.find(data,{"_id":False})   
        return data_read
    
    # Update method to update items within the Bid database.
    def update(self, query, data):
        if data is not None:    
            data_update = self.database.items.update_one(query, data)
            return data_update
        else:
            raise Exception("Nothing to update because data parameter is incorrectly formatted")
          
    # Delete method to remove items from the Bid database.
    def delete(self,data):
        if data is not None:    
            data_delete = self.database.items.delete_one(data)
            return data_delete
        else:
            raise Exception("Nothing to delete because data parameter is incorrectly formatted")
