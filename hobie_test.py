from re import X
from pymongo import MongoClient
port = 42042

client = MongoClient("localhost", int(port))
db = client['291db']


def test1():
    global db
    tp = db['title_principals']
    print(list(tp.find({'category':'test'})))


def test2():
    global db
    tp = db['title_principals']
    tp.delete_one({'category': 'test'})

def test3():
    global db
    print(db.list_collection_names())

def main():
    test1()


main()


