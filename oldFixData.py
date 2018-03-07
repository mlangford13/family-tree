# fix data
from mongoengine import *
from dbDef import *
from utility import *
from userStories import *
import datetime
import argparse

parser = argparse.ArgumentParser(description='Detect and delete bad records in the database.')
parser.add_argument('-v',action='store_true',help='Verbose output.')
parser.add_argument('-t',action='store_true',help='Use the test database.')
parser.add_argument('-d',action='store_true',help='Delete bad objects and ids.')
args = parser.parse_args()

debug = args.v
test = args.t
delete = args.d
if test:
    connectToTest()
    if debug:
        print("Connected to Test Database")
else:
    connectToMongoDB()
    if debug:
        print("Connected to Main Database")

def findBad():
    badIds = []
    for i in Indi.objects:
        valid = True
        # US01 date before today
        if(not dateBeforeToday(i)):
            if debug: print("Error US01("+i.pid + "): a date is in the future.")
            valid = False
        # US02 Birth before marriage
        if(not birthBeforeMarriage(i)):
            if debug: print("Error US02("+i.pid + "): marriage occurs before birth.")
            valid = False
        # US03 Birth before death
        if(not birthBeforeDeath(i)):
            if debug: print("Error US03("+i.pid + "): death occurs before birth.")
            valid = False
        # US04 Marriage before divorce
        if(not marriageBeforeDivorce(i)):
            if debug: print("Error US04("+i.pid + "): divorce occurs before marriage.")
            valid = False
        # US05 Marriage before death
        if(not marriageBeforeDeath(i)):
            if debug: print("Error US05("+i.pid + "): death occurs before marriage.")
            valid = False
        # US06 Divorce before death
        if(not divorceBeforeDeath(i)):
            if debug: print("Error US06("+i.pid + "): divorce occurs after death.")
            valid = False
        # US07 Less than 150 years old
        if(not isLessThan150(i)):
            if debug: print("Error US07("+i.pid + "): age >= 150 years.")
            valid = False
        # US10 Marriage after 14
        if(not marriageAfter14(i)):
            if debug: print("Error US10("+i.pid + "): marriage before 14.")
            valid = False
        if not valid:
            if i.pid not in badIds:
                badIds.append(i.pid)
    return badIds

# return list of fids with not parents or children
def emptyFams():
    output = []
    for f in Fam.objects:
        if f.wid == '' and f.hid == '' and f.children == []:
            output.append(f.fid)
    return output
# removes fams from records
# takes a list of fids
def removeFams(famList):
    for f in Fam.objects:
        if f.fid in famList: f.delete()
    for i in Indi.objects:
        for key in i.marriages:
            if key in famList:
                i.marriages.pop(key)
        for key in i.divorces:
            if key in famList:
                i.divorces.pop(key)

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
        f.save()
        badChildren = []
        # children
        if f.children != []:
            for pid in f.children:
                if pid in idList:
                    badChildren.append(pid)
        for child in badChildren:
            f.children.remove(child)

badIds = findBad()
if debug:
    if badIds == []: print("No bad ids.")
    else: print("Bad Ids: "+str(badIds))
if delete:
    while badIds != []:
        removeIds(badIds)
        badFams = emptyFams()
        removeFams(badFams)
        badIds = findBad()
