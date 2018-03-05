# check for errors
from mongoengine import *
from dbDef import *
from utility import *
from userStories import *
import datetime

connectToMongoDB()

for i in Indi.objects:
    # US01 date before today
    if(not dateBeforeToday(i)):
        print("Error: "+str(i.pid)+" date is in the future.")
    # US02 Birth before marriage
    if(not birthBeforeMarriage(i)):
        print("Error: "+str(i.pid)+" marriage before birth.")
    # US03 Birth before death
    if(not birthBeforeDeath(i)):
        print("Error: "+str(i.pid)+" death before birth.")
    # US04 Marriage before divorce
    if(not marriageBeforeDivorce(i)):
        print("Error: "+str(i.pid)+" divorce before marriage.")
    # US05 Marriage before death
    if(not marriageBeforeDeath(i)):
        print("Error: "+str(i.pid)+" death before marriage.")
    # US06 Divorce before death
    if(not divorceBeforeDeath(i)):
        print("Error: "+i.pid+" divorce after death.")
    # US07 Less than 150 years old
    if(not isLessThan150(i)):
        print("Error: "+i.pid+" over 150 years old.")
