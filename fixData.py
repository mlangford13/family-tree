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

def findBadIndis():
    badIds = []
    for i in Indi.objects:
        valid = True
        # US01 date before today
        if(not dateBeforeToday(i)):
            if debug: print("Error ("+i.pid + "): a date is in the future.")
            valid = False
        # US02 Birth before marriage
        if(not birthBeforeMarriage(i)):
            if debug: print("Error ("+i.pid + "): marriage occurs before birth.")
            valid = False
        # US03 Birth before death
        if(not birthBeforeDeath(i)):
            if debug: print("Error ("+i.pid + "): death occurs before birth.")
            valid = False
        # US04 Marriage before divorce
        if(not marriageBeforeDivorce(i)):
            if debug: print("Error ("+i.pid + "): divorce occurs before marriage.")
            valid = False
        # US05 Marriage before death
        if(not marriageBeforeDeath(i)):
            if debug: print("Error ("+i.pid + "): death occurs before marriage.")
            valid = False
        # US06 Divorce before death
        if(not divorceBeforeDeath(i)):
            if debug: print("Error ("+i.pid + "): divorce occurs after death.")
            valid = False
        # US07 Less than 150 years old
        if(not isLessThan150(i)):
            if debug: print("Error ("+i.pid + "): age >= 150 years.")
            valid = False
        # US10 Marriage after 14
        if(not marriageAfter14(i)):
            if debug: print("Error ("+i.pid + "): marriage before 14.")
            valid = False
        if not valid:
            if i.pid not in badIds:
                badIds.append(i.pid)
    return badIds

# return list of fids that are not valid
def findBadFams():
    badIds = []
    for f in Fam.objects:
        valid = True

        # no parents and children
        if f.wid == '' and f.hid == '' and f.children == []:
            if debug: print("Error ("+f.fid + "): family has no parents or children.")
            valid = False

        # US08 birth after marriage of parents
        if(not birthAfterMarriageOfParents(f)):
            if debug: print("Error ("+f.fid + "): birth occurs before marriage of parents.")
            valid = False
        # US09 birth before death of parents
        if(not birthBeforeDeathOfParents(f)):
            if debug: print("Error ("+f.fid + "): birth occurs after death of parents.")
            valid = False

        # US12 parents not too old
        if(not parentsNotTooOld(f)):
            if debug: print("Error ("+f.fid + "): parents are too old for children.")
            valid = False

        # US13 sibling spacing
        if(not siblingSpacing(f)):
            if debug: print("Error ("+f.fid + "): children spacing is too close but not twins.")
            valid = False

        # US15 too many siblings
        if(tooManySiblings(f)):
            if debug: print("Error ("+f.fid + "): too many (>= 15) children.")
            valid = False

        # US16 males last names in the family
        if(not same_male_last_names(f)):
            if debug: print("Error ("+f.fid + "): male child does not have the correct last name.")
            valid = False

        # US18 siblings should not marry
        if(siblingMarriages(f)):
            if debug: print("Error ("+f.fid + "): siblings are married.")
            valid = False

        # US25 unique first name in families
        if(not uniqueFirstNames(f)):
            if debug: print("Error ("+f.fid + "): first names are not unique.")
            valid = False


        if not valid:
            if f.fid not in badIds:
                badIds.append(f.fid)
    return badIds
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
def removeIndis(idList):
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
        f.save()

badIds = findBadIndis()
if debug:
    if badIds == []: print("No bad ids.")
    else: print("Bad Ids: "+str(badIds))
if delete:
    while badIds != []:
        removeIndis(badIds)
        badFams = findBadFams()
        removeFams(badFams)
        badIds = findBadIndis()
