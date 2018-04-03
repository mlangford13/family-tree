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
    return Fam.objects.get(fid=fid)

def getFams(fids):
    fams = []
    for fid in fids:
        fams.append(getFam(fid))
    return fams

def getFam(fid):
    return Fam.objects.get(fid=fid)

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

def getSurvivingDescendants(indi):
    descendants = []
    cids = indi.children
    children = getIndis(cids)
    for child in children:
        if child.alive:
            print("Child: " + child.pid)
            descendants.extend(child.pid) #Put child on
        temp = getSurvivingDescendants(child)
        if temp:
            descendants.extend(temp)

    return descendants

def clearDB():
    # Delete old data
    for i in Indi.objects:
        i.delete()
    for i in Fam.objects:
        i.delete()
