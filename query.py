from mongoengine import *

# connect to MongoDB with pymongo
connect('test', host='localhost', port=27017)


GENDERS = ['M','F','O'] # male female other

class Indi(Document):
    pid = StringField(required=True,primary_key=True) # identifier
    name = StringField()
    gender = StringField(choices=GENDERS) # male, female, or other
    birth = StringField() # birthday
    age = IntField()
    alive = BooleanField() # are they currently alive
    death = StringField() # when did they die? not required
    children = ListField(StringField()) # list of children ids
    marriages = DictField() # pid of spouse: date of marriage
    divorces = DictField() # pid of ex : date of divorce
    families = ListField(StringField()) # list of family ids

for i in Indi.objects():
    print(i.pid)
