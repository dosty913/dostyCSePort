# Daniel Ostrin 1/30/2021

from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
    def __init__(self, username, password):
        self.client = MongoClient('mongodb://%s:%s@localhost:29024/?authMechanism=DEFAULT&authSource=AAC'%(username, password)) 
        self.database = self.client['AAC']

    # Create method to implement the C in CRUD
    def create(self, data):
        if data is not None:
            self.database.animals.insert(data) # data should be dictionary
            return True
        else:
            print('Nothing to save, because data parameter is empty')
            return False

    # Read method to implement the R in CRUD
    def read(self, data):
        if data is not None:
            return self.database.animals.find(data,{"_id":False})
        else:
            print('Nothing to read, because data parameter is empty')
            return False
    
    # Update method to implement the U in CRUD
    def update(self, data, change):
        if data is not None:
            return self.database.animals.update(data,{ "$set": change}) # data and change are dictionaries
        else:
            print('Nothing to update, because data parameter is empty')
            return False
            
    # Delete method to implement the D in CRUD
    def delete(self, data):
        if data is not None:
            return self.database.animals.delete_one(data) # data is dictionary 
        else: 
            print('Nothing to delete, because data parameter is empty')
            return False