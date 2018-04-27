from mongoengine import *
from dbDef import *
import datetime
import calendar

def getIndi(pid):
    try:
        return Indi.objects.get(pid=pid)
    except:
        return None

def getIndis(pids):
    indis = []
    for pid in pids:
        indi = getIndi(pid)
        if indi != None:
            indis.append(indi)

    return indis

def getFam(fid):
    try:
        return Fam.objects.get(fid=fid)
    except:
        return None

def getFams(fids):
    fams = []
    for fid in fids:
        family = getFam(fid)
        if family != None:
            fams.append(family)
    return fams

def addMonths(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.datetime(year,month,day)

def getSpousesOfIndi(i):
    families = getFams(i.marriages.keys())
    spouses = []
    for fam in families:
        spouse = None
        if i.gender == 'M':
            spouse = getIndi(fam.wid)
        else:
            spouse = getIndi(fam.hid)

        if spouse != None:
            spouses.append(spouse)

    return spouses

def getSpousePids(i):
    families = getFams(i.marriages.keys())
    spouses = []
    for fam in families:
        spouse = None
        if i.gender == 'M':
            spouse = fam.wid
        else:
            spouse = fam.hid
        spouses.append(spouse)

    return spouses

def getChildrenOfIndi(i):
    families = getFams(i.marriages.keys())
    children = []
    for fam in families:
        children.extend(getIndis(fam.children))
    return children

# Recursive Helper function for US37
def getSurvivingDescendants(indi):
    descendants = []
    children = getChildrenOfIndi(indi)

    for child in children:
        if child.alive:
            descendants.append(child.pid) #Put child on
        temp = getSurvivingDescendants(child)
        if temp:
            descendants.extend(temp)

    return descendants

# Recursive Helper function for US17
def getDescendants(indi):
    descendants = []
    children = getChildrenOfIndi(indi)

    for child in children:
        descendants.append(child.pid) #Put child on
        temp = getDescendants(child)
        if temp:
            descendants.extend(temp)

    return descendants

def clearDB():
    # Delete old data
    for i in Indi.objects:
        i.delete()
    for i in Fam.objects:
        i.delete()
