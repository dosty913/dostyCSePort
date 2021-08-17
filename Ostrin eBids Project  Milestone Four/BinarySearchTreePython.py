# imports
import csv
import json
from pprint import pprint
import pandas as pd
import sys, getopt, pprint, os
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


# THIS SECTION ONLY NEEDED FOR INITIAL SETUP

# Setup to import the csv file into mongodb through mongodb atlas
#def import_content(filepath):

    # Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
#    client = pymongo.MongoClient("mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority")
    # details for the database and collection names
#    mng_db = client['mongodb_eBids']
#    collection_name = 'eBids'
#    db_cm = mng_db[collection_name]
    # setup to pull the data from csv file and insert into mongodb as json data
#    cdir = os.path.dirname(__file__)
#    file_res = os.path.join(cdir, filepath)
#    data = pd.read_csv(file_res)
#    data_json = json.loads(data.to_json(orient='records'))
#    db_cm.remove()
#    db_cm.insert(data_json)

#if __name__ == "__main__":
#    filepath = 'eBids.csv'
#    import_content(filepath)

# THIS SECTION ONLY NEEDED FOR INITIAL SETUP 

# Provide the mongodb atlas url to connect python to mongodb using pymongo and create a connection using MongoClient
connectMongo = "mongodb+srv://myAdminUser:abcd1234@cluster0.xvstd.mongodb.net/mongodb_eBids?retryWrites=true&w=majority"

# Create the database for our example (we will use the same database throughout the tutorial
client = pymongo.MongoClient(connectMongo)

# set our actual database to db
mydb = client.mongodb_eBids
mycol = mydb.eBids

#    # Create method to add new items to the Bid database.
#    def create(self, data):
#        if data is not None:
#            data_create = mycol.insert_one(data)  # data should be dictionary
#            return data_create
#        else:
#            raise Exception("Nothing to save, because data parameter is incorrectly formatted")

    # Read method to find one or all items within the Bid database.
#    def read(self,data):
#        if data is not None:    
#            data_read = mycol.find_one(data,)
#            return data_read
#        else:
#            raise Exception("Nothing to read because data parameter is incorrectly formatted")
#    def readAll(self, data):    
#        data_read = self.database.items.find(data,{"_id":False})   
#        return data_read
    
   # Update method to update items within the Bid database. 
#    def update(self, query, data):
#        if data is not None:    
#            data_update = self.database.items.update_one(query, data)
#            return data_update
#        else:
#            raise Exception("Nothing to update because data parameter is incorrectly formatted")
          
    # Delete method to remove items from the Bid database.
#    def delete(self,data):
#        if data is not None:    
#            data_delete = self.database.items.delete_one(data)
#            return data_delete
#        else:
#            raise Exception("Nothing to delete because data parameter is incorrectly formatted")

# *** Testing type things to ensure proper connection and access ***

newBid = ({
    'Auction Title' : "Dell Laptop w/Bag",
    'Auction Id' : 79533,
    'Department' : "ITS",
    'Close Date' : "11/26/2013",
    'Winning Bid' : "$79.51 ",
    'CC Fee' : "$2.81 ",
    'Fee Percent' : 0.23,
    'Auction Fee Subtotal' : "$128.05 ",
    'Auction Fee Total' : "$18.25 ",
    'Pay Status' : "Successful",
    'Paid Date' : "1/3/2014",
    'Asset #' : '',
    'Inventory ID' : "75576",
    'Decal /Vehicle ID' : '',
    'VTR Number' : '',
    'Receipt Number' : "3604198592",
    'Cap' : "$3,000 ",
    'Expenses' : "$0.00 ",
    'Net Sales' : "$60.45 ",
    'Fund' : "General Fund",
    'Business Unit' : 0 
    })

print(mydb.list_collection_names())

print(mycol.count_documents({}))

# working on the menu options to incorportate the CRUD functions

def menu():
    print("1. Add a Bid record")
    print("2. Search for a bid record")
    print("3. Modify a bid record")
    print("4. Delete a bid record")
    print("0. Exit Menu")

menu()
while True:
    try:
        option = int(input("Please Select an Option: "))
        if option == 1:
            mycol.insert_one(newBid)
            print("\n Bid Record Added!")
        elif option == 2:
            for x in mycol.find().limit(5):
                pprint.pprint(x)
            print("\n Bid Records Found!")
        elif option == 3:
            print("\n Bid Record Modified") 
        elif option == 4:
            removalTest = mycol.delete_one({})
            print("\n Bid Record Deleted") 
        elif option == 0:
            break
        else:
            print("\n Not a Valid Option Please Try again")
    except ValueError:
        print("\n Not a Valid Option Please Try again")

    print()
    print(mydb.list_collection_names())
    print(mycol.count_documents({}))

    menu()
    option = int(input("Please Select an Option: "))

print("Thank you. Goodbye.")



