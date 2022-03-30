
from pymongo import MongoClient


def main():
    global db
    # port = input("Input a port number: ")
    port = 42042

    client = MongoClient("localhost", int(port))
    db = client['291db']
    menu()


def menu():
    while True:
        print('-'*10)
        print('MAIN MENU')
        print('-'*10)
        print('1. Search for titles')
        print('2. Search for genres')
        print('3. Search for cast/crew members')
        print('4. Add a movie')
        print('5. Add a cast/crew member')
        while True:
            op = input(
                'Enter a number to select an option\nor press enter to end program: ')
            if op in ['1', '2', '3', '4', '5', '']:
                break
            print('Invalid option.')
        if op == '1':
            pass
        elif op == '2':
            pass
        elif op == '3':
            pass
        elif op == '4':
            flag = addMovie()
        elif op == '5':
            flag = addMember()
        if flag == 1:
            break


def addMovie():
    global db
    col = db['title_basics']
    while True:         # get a unique ID
        id = input('Please enter a unique ID\nor press enter to abort: ')
        if id == '':
            return 0
        rslt = list(col.find({'tconst': id}))
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
            if int(runtime) > 0:
                break
        print('The entered running time is invalid.')
    runtime = int(runtime)
    while True:         # get a valid list of genres
        genres = input(
            'Please enter up to 3 genres seperated by commas\nor enter 0 to set to Null\nor press enter to abort: ')
        if genres == '':
            return 0
        if genres == '0':
            genres = None
            break
        genres = genres.split(',')
        if len(genres) in range(1, 4):
            for i in range(len(genres)):
                genres[i] = genres[i].strip()
            break
        else:
            print('Invalid number of genres.')
    movie = {
        "tconst": id,
        "titleType": "movie",
        "primaryTitle": title,
        "originalTitle": title,
        "isAdult": '\\N',
        "startYear": sYear,
        "endYear": '\\N',
        "runtimeMinutes": runtime,
        "genres": genres}

    col.insert_one(movie)

    print('Movie added successfully!')
    while True:
        flag = input('1. Return to main menu\n2. End program\nOption: ')
        if flag == '1':
            return 0
        elif flag == '2':
            return 1
        print('Invalid option.')


def addMember():
    global db
    nb = db['name_basics']
    tb = db['title_basics']
    tp = db['title_principals']
    while True:         # get a valid cast/crew member id
        mid = input(
            'Please enter a cast/crew member id\nor press enter to abort: ')
        if mid == '':
            return 0
        rslt = list(nb.find({'nconst': mid}))
        if rslt != []:
            break
        print('The cast/crew member does not exist.')
    while True:
        tid = input(
            'Please enter a title id\nor press enter to abort: ')
        if tid == '':
            return 0
        rslt = list(tb.find({'tconst': tid}))
        if rslt != []:
            break
        print('The title does not exist.')
    category = input('Please enter a category\nor press enter to abort: ')
    if category == '':
        return 0
    castNCrew = list(tp.aggregate([
        {'$match': {'tconst': tid}},
        {'$group': {'_id': '$tconst', 'maxOrd': {'$max': '$ordering'}}}
    ]))
    if castNCrew == []:
        ord = 1
    else:
        ord = castNCrew[0]['maxOrd']+1
    newMember = {
        "tconst": tid,
        "ordering": ord,
        "nconst": mid,
        "category": category,
        "job": '\\N',
        "characters": ["\\N"]}

    tp.insert_one(newMember)

    print('cast/crew member added successfully!')
    while True:
        flag = input('1. Return to main menu\n2. End program\nOption: ')
        if flag == '1':
            return 0
        elif flag == '2':
            return 1
        print('Invalid option.')


if __name__ == "__main__":
    main()
