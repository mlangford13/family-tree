from mongoengine import *
from dbDef import Indi, DATABASE

# connect to MongoDB with pymongo
connect(DATABASE, host='localhost', port=27017)

# query Indi collection
for i in Indi.objects():
    print(i.pid)
