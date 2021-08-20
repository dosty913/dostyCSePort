# imports
import csv
import json
import pandas as pd
import sys, getopt, pprint, os
import pymongo
from pymongo import MongoClient

# Setup to import the csv file into mongodb through mongodbatlas
def import_content(filepath):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
    client = pymongo.MongoClient("mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority")
    # details for the database and collection names
    mng_db = client['mongodb_eBids']
    collection_name = 'eBids'
    db_cm = mng_db[collection_name]
    # setup to pull the data from csv file and insert into mongodb as json data
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)
    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)

if __name__ == "__main__":
    filepath = 'eBids.csv'
    import_content(filepath)

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
    client = pymongo.MongoClient("mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority")
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['eBids']
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    # Get the database
    dbname = get_database()


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