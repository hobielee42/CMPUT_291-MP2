
from xml.etree.ElementTree import TreeBuilder
from pymongo import MongoClient

# port = input("Input a port number: ")
port = 42042

client = MongoClient("localhost", int(port))
db = client['291db']


def main():
    addMovies()


def addMovies():
    global client, db
    title_basics = db['title_basics']
    while True:         # get a unique ID
        id = input('Please enter a unique ID\nor press enter to abort: ')
        if id == '':
            return 0
        rslt = list(title_basics.aggregate([
            {'$match': {'tconst': id}},
            {'$count': 'count'}
        ]))
        if rslt == []:
            break
        print('The entered ID is not unique.')
    title = input('Please enter a title\nor press enter to abort: ')
    if title == '':
        return 0
    while True:         # get a valid start year
        sYear = input('Please enter a start year\nor press enter to abort: ')
        if sYear == '':
            return 0
        if sYear.isdecimal():
            break
        print('The entered year is invalid.')
    sYear = int(sYear)
    while True:         # get a valid running time
        runtime = input(
            'Please enter a running time\nor press enter to abort: ')
        if runtime == '':
            return 0
        if runtime.isdecimal():
            if runtime > 0:
                break
        print('The entered running time is invalid.')
    runtime = int(runtime)
    while True:         # get a valid list of genres
        genres = input(
            'Please enter up to 3 genres seperated by commas\nor press enter to abort: ')
        if genres == '':
            return 0
        genres = genres.split(',')
        if len(genres)
        for i in range(len(genres)):
            genres[i] = genres[i].strip()


if __name__ == "__main__":
    main()
