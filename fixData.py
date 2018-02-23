# fix data
from mongoengine import *
from dbDef import *
from utility import *
from userStories import *
#import unittest
import datetime

connectToMongoDB()


# print if fam has parents that are too old
# for i in Fam.objects:
#     if(not parentsNotTooOld(i)):
#         print(i.fid + " has a parent/parents that is/are too old for their children")

# removes indis that don't pass test
#for i in Indi.objects:
#    if(not birthBeforeDeath(i)):i.delete()

# print pid of indis that don't pass test
for i in Indi.objects:
    if(not birthBeforeDeath(i)):print(i.pid + " dies before they are born.")
