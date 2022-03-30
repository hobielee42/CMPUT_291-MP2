from pymongo import MongoClient
port = 42042


# client = MongoClient("localhost", int(port))
# db = client['291db']
# title_basics = db['title_basics']
# while True:
#     id = input('Please enter a unique ID: ')
#     rslt = list(title_basics.aggregate([
#         {'$match': {'tconst': id}},
#         {'$count': 'count'}
#     ]))
#     print(rslt)

tsts = '   fdsfe   ,dsfeef,sgfge  fdsfe,fse,  fef '.split(',')
for i in range(len(tsts)):
    tsts[i] = tsts[i].strip()
print(tsts)
