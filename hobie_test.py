from re import X
from pymongo import MongoClient
port = 42042

client = MongoClient("localhost", int(port))
db = client['291db']


def test1():
    global db
    col = db['title_principals']
    print(list(col.find({'tconst':'tt0073537'})))


def test2():
    global db
    col = db['title_basics']
    col.delete_one({'tconst': 'test'})

def test3():
    global db
    print(db.list_collection_names())

def main():
    test1()


main()


