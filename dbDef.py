# Database Definitions
from mongoengine import *

global DATABASE, GENDERS
DATABASE = 'test'
GENDERS = ['M','F','O'] # male female other

# TODO: make default value for alive true
# TODO : change string fields to date fields where it is needed

def connectToMongoDB():
    connect(DATABASE, host='localhost', port=27017)

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

class Fam(Document):
    fid = StringField(required=True,primary_key=True)
    married = StringField()
    divorced =StringField()
    hid =StringField()
    wid =StringField()
    children =ListField()
