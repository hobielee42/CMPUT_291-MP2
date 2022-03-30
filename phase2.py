
from pymongo import MongoClient


def main():
    global db
    port = input("Input a port number: ")
    # port = 27017

    client = MongoClient("localhost", int(port))
    db = client['291db']
    menu()


def menu():
    while True:
        flag = 0
        print('\n'+'-'*10)
        print('MAIN MENU')
        print('-'*10)
        print(
            '''1. Search for titles
2. Search for genres
3. Search for cast/crew members
4. Add a movie
5. Add a cast/crew member
''')
        while True:
            op = input(
                'Enter a number to select an option\nor press enter to end program: ')
            if op in ['1', '2', '3', '4', '5', '']:
                break
            print('Invalid option.')
        if op == '1':
            flag = search()
        elif op == '2':
            genres_search()
        elif op == '3':
            cast_search()
        elif op == '4':
            flag = addMovie()
        elif op == '5':
            flag = addMember()
        elif op == '':
            break
        if flag == 1:
            break


def cast_search():
    global db
    name_basics = db["name_basics"]
    title_basics = db["title_basics"]
    title_principals = db["title_principals"]
    while(1):
        inp = input('''
To go back to menu type 'back'
To search for a cast/crew member enter their name here: ''')
        list_of_cast = []
        if inp.lower() == 'back':
            return
        if inp.lower() == 'back':
            return
        key_words = inp.split()
        search = {}
        dic_list = []
        for word in key_words:
            search = {}
            dick = {}
            dick['$regex'] = '.*' + word + '.*'
            dick['$options'] = '-i'
            search['primaryName'] = dick
            dic_list.append(search)
        casts = name_basics.find({'$and': dic_list})
        for cast in casts:
            dic_list = []
            search = {}
            list_of_cast.append(cast)
            for title in cast['knownForTitles']:
                if title != '\\N':
                    search['tconst'] = title
                    dic_list.append(search)
            print(cast['primaryName'], ' :')
            
            if len(dic_list) > 0:
                movies = title_basics.find({'$or': dic_list})
                for movie in movies:
                    print('movie title { ', movie['primaryTitle'], '} :')
                    people = title_principals.find(
                        {'$and': [{'tconst': movie['tconst']}, {'nconst': cast['nconst']}]})
                    for person in people:
                        print('    job:',
                              person['category'], person['characters'])
            #else:
            #    print(' No Movies ')
            print('')


def genres_search():
    global db
    title_basics = db['title_basics']
    genres = title_basics.distinct("genres")
    while(1):
        free = 0
        x = 'd'
        inp = input('''
To go back to menu type 'back'
To search for a genre enter here: ''')
        if inp.lower() == 'back':
            return
        for cat in genres:
            if inp.lower() == cat.lower():
                free = 1
        if free == 0:
            x = 'back1'
            print("That is not a value genre\n")
        genre = inp.lower()
        isnumber = False
        while(not isnumber and x != 'back1'):
            inp = input('''
To go back to menu type 'back'
to search for a different genre type 'genre'
enter a minimum vote count: ''')
            if inp.lower() == 'back':
                return
            if inp.lower() == 'genre':
                x = 'back1'
            if ord(inp[0]) >= 48 and ord(inp[0]) <= 57:
                isnumber = True
                votes = int(inp)
            else:
                print("Please input a number")
        if x != 'back1':

            big_list = []
            #mov_list = db.title_ratings.aggregate([ {"$lookup": { "from": 'title_basics', 'localField': 'tconst', 'foreignField': 'tconst', 'as': 'title'}}]).sort("averageRating", -1)
            #mov_list = db.title_basics.aggregate([{'$unwind': '$genres'},
            #                                     {'$match': {'$expr': {'$eq': [genre, {'$toLower': '$genres'}]}}}, {'$lookup': {'from': 'title_ratings', 'localField': 'tconst', 'foreignField': 'tconst', 'as': 'good_rate'}}, {'$sort': {'good_rate.averageRating': -1}}])

            mov_list = db.title_basics.aggregate([{"$lookup": {"from": "title_ratings", "let": {"field": "$tconst"}, "pipeline": [], "localField": "tconst", "foreignField": "tconst", "as": "good_rate"}},
                                                  {'$unwind': '$genres'},
                                                 {'$match': {'$expr': {'$eq': [genre, {'$toLower': '$genres'}]}}}, {'$sort': {'good_rate.averageRating': -1}}])            
    
            for mov in mov_list:
                for rate in mov['good_rate']:
                    if rate['numVotes'] > votes:
                        print('Title : ', mov['primaryTitle'], ', rating:', rate['averageRating'], ', Votes:', rate['numVotes'])


def search():
    global db
    name_basics = db['name_basics']
    title_basics = db['title_basics']
    title_principals = db['title_principals']
    title_ratings = db['title_ratings']
    while(1):
        x = ""
        inp = ""
        while(len(inp) <= 0):
            inp = input('''
To go back to menu type 'back'
To search for a movie enter key words here: ''')
        if inp.lower() == 'back':
            return
        key_words = inp.split()
        search = {}
        dic_list = []
        for word in key_words:
            if len(word) == 4 and (ord(word[0]) >= 48 and ord(word[0]) <= 57) and (ord(word[1]) >= 48 and ord(word[1]) <= 57) and (ord(word[2]) >= 48 and ord(word[2]) <= 57) and (ord(word[3]) >= 48 and ord(word[3]) <= 57):
                counter = 0
                for letter in word:
                    if ord(letter) >= 48 and ord(letter) <= 57:
                        counter = counter + 1
                if counter == 4:
                    search['startYear'] = int(word)
            else:
                enter = 0
                search = {}
                dick = {}
                dick['$regex'] = '.*' + word + '.*'
                for letter in word:
                    if ord(letter) >= 48 and ord(letter) <= 57:
                        enter = 1
                if enter == 0:
                    dick['$options'] = '-i'
                search['primaryTitle'] = dick

            dic_list.append(search)
        print(dic_list)
        while(x != "back2"):
            x = 'd'
            movies = title_basics.find({'$and': dic_list})
            movie_list = []
            count = 1
            for mov in movies:
                print(count, ": ", mov["tconst"], "|", mov["titleType"], "|", mov["primaryTitle"], "| Original title:", mov["originalTitle"],
                      "| Is adult:", mov["isAdult"], "| Start/End year:", mov["startYear"], mov["endYear"], "| Runtime (min):", mov["runtimeMinutes"], "|", mov["genres"])
                movie_list.append([mov["tconst"], mov["primaryTitle"]])
                print()
                count = count + 1
            if count == 1:
                print("\nThere are no movies that fit those extact search inputs")
                x = 'back2'
            inp = "d"
            while(not(ord(inp[0]) >= 48 and ord(inp[0]) <= 57) and x != 'back2'):
                while(inp == "d" or len(inp) <= 0):
                    inp = input('''
to go back to main menu type 'back'
to preform another search type 'search'
to select a title enter the number that appeared by the movie: ''')
                if inp.lower() == 'back':
                    return
                if inp.lower() == 'search':
                    x = 'back2'
            if (x != 'back2'):
                inp = int(inp)

                selected_movie = movie_list[inp - 1][0]

                print(selected_movie)

                rate_votes = title_ratings.find({'tconst': selected_movie})
                peoples = title_principals.find({'tconst': selected_movie})

                people_list = []
                for people in peoples:
                    crew = []
                    crew.append(people["category"])
                    characters = name_basics.find({'nconst': people['nconst']})
                    for character in characters:
                        crew.append(character['primaryName'])
                    crew.append(people["characters"])
                    people_list.append(crew)

                print("\n------", movie_list[inp - 1][1], "-------")

                for rate_vote in rate_votes:
                    print(
                        "Rating: ", rate_vote["averageRating"], "\nVotes:", rate_vote["numVotes"])
                for people in people_list:
                    print(people[0], ": ", people[1], "   Character: ", people[2])

                inp = ''
                while(x != "back1" and x != "back2"):
                    while(len(inp) <= 0):
                        inp = input('''
to go back to main menu type 'back'
to search again enter 1
to select another title from you previous search enter 2: ''')
                    if ord(inp[0]) == 49:
                        x = "back2"
                    if ord(inp[0]) == 50:
                        x = "back1"
                    if inp.lower() == 'back':
                        return


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
