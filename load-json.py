import json

from pymongo import MongoClient

fileNames = ["name.basics.json", "title.basics.json", "title.principals.json", "title.ratings.json"]

port = input("Input a port number: ")

# assume server is on your own machine
client = MongoClient("localhost", int(port))

def main():
    global client, fileNames
    
    db = client["291db"]
    
    # get the four collections, dropping if exists
    # then add data to collections
    # input files are humongous so iterate over every line
    collections = {}
    for fileName in fileNames:
    
        print("processing file " + fileName + "...")
    
        # might not need this but i'm not sure if pymongo's dict is efficient to access over and over
        collectionName = fileName.rstrip("json").rstrip(".").replace(".", "_")
        collections[fileName] = db[collectionName]
        collections[fileName].drop()
        
        data = None
        with open(fileName, encoding="utf-8") as file:
            # this takes SO LONG
            for line in file:
                line = line.strip("[],\n")
                if line != "":
                    collections[fileName].insert_one(json.loads(line))
        
    client.close()


if __name__ == "__main__":
    main()