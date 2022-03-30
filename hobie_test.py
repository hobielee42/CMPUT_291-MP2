from pymongo import MongoClient
port = 42042

client = MongoClient("localhost", int(port))
db = client['291db']


def test1():
    global db
    tb = db['title_basics']
    print(list(tb.find({'tconst': 'test'})))


def test2():
    global db
    tb = db['title_basics']
    tb.delete_one({'tconst': 'test'})


def main():
    test2()


main()
