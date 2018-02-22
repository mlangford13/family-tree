# Database Definitions
from mongoengine import *

global DATABASE, GENDERS
DATABASE = 'test'
GENDERS = ['M','F','O'] # male female other


def connectToMongoDB():
    connect(DATABASE, host='localhost', port=27017)

class Indi(Document):
    pid = StringField(required=True,primary_key=True) # identifier
    name = StringField()
    gender = StringField(choices=GENDERS) # male or female ('M' or 'F')
    birth = DateTimeField() # birthday
    age = IntField()
    alive = BooleanField(default=True) # are they currently alive
    death = DateTimeField() # when did they die? not required
    children = ListField(StringField()) # list of children ids (seems to be wrong and had fids)
    marriages = DictField() # pid of spouse: date of marriage
    divorces = DictField() # pid of ex : date of divorce
    families = ListField(StringField()) # list of family ids

class Fam(Document):
    fid = StringField(required=True,primary_key=True)
    married = DateTimeField()
    divorced = DateTimeField()
    hid = StringField()
    wid = StringField()
    children = ListField(StringField()) # list of child pids
