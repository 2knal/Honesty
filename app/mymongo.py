from pymongo import MongoClient

import json, pprint
client = MongoClient('localhost', 27017)

with open('users.json', 'r') as fp:
    data = json.load(fp)
    #print(data)
users = []

users = data['id']
print(users)

db = client.user_data
result = db.users.insert_many(users)


result1= db.users.find({})
pprint.pprint(result1[0])
