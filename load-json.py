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
            # need to try to change this; loading 60mb into memory is hyper bad
            data = json.load(file)

#            for line in file:
#                if "[" not in line:
#                    line = line.strip()
#                    collections[fileName].insert_one(json.loads(line))

        collections[fileName].insert_many(data)
        if "name" not in fileName:
            collections[fileName].create_index([("tconst", 1)])
        
    db["title_ratings"].create_index([("numVotes", 1)])
    db["name_basics"].create_index([("primaryName", 1)])
    db["title_basics"].create_index([("primaryTitle", 1)])
        
    client.close()


if __name__ == "__main__":
    main()