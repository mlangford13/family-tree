# fix data
from mongoengine import *
from dbDef import *
from utility import *
from userStories import *
import datetime

connectToMongoDB()


# print if fam has parents that are too old
# for i in Fam.objects:
#     if(not parentsNotTooOld(i)):
#         print(i.fid + " has a parent/parents that is/are too old for their children")

# removes indis that don't pass test
#for i in Indi.objects:
#    if(not birthBeforeDeath(i)):i.delete()

def findBad():
    badIds = []
    for i in Indi.objects:
        valid = True
        # US01 date before today
        if(not dateBeforeToday(i)):
            valid = False
        # US02 Birth before marriage
        if(not birthBeforeMarriage(i)):
            valid = False
        # US03 Birth before death
        if(not birthBeforeDeath(i)):
            valid = False
        # US04 Marriage before divorce
        if(not marriageBeforeDivorce(i)):
            valid = False
        # US05 Marriage before death
        if(not marriageBeforeDeath(i)):
            valid = False
        # US06 Divorce before death
        if(not divorceBeforeDeath(i)):
            valid = False
        # US07 Less than 150 years old
        if(not isLessThan150(i)):
            valid = False
        if not valid:
            if i.pid not in badIds:
                badIds.append(i.pid)
    return badIds

# removes ids from records
# takes the list of ids
def removeIds(idList):
    for i in Indi.objects:
        # children
        badChildren = []
        if i.children != []:
            for pid in i.children:
                if pid in idList:
                    badChildren.append(pid)
        for child in badChildren:
            i.children.remove(child)

        # marriages
        for pid in i.marriages:
            if pid in idList:
                i.marriages.pop(pid)
        # divorces
        for pid in i.divorces:
            if pid in idList:
                i.divorces.pop(pid)
        if i.pid in idList:
            i.delete()

    for f in Fam.objects:
        # hid
        if f.hid in idList: f.hid = ''
        # wid
        if f.wid in idList: f.wid = ''

        badChildren = []
        # children
        if f.children != []:
            for pid in f.children:
                if pid in idList:
                    badChildren.append(pid)
        for child in badChildren:
            f.children.remove(child)

badIds = findBad()
print(badIds)
while badIds != []:
    removeIds(badIds)
    badIds = findBad()
    print(badIds)
