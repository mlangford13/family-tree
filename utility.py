from mongoengine import *
from dbDef import *
import datetime
import calendar

def getIndi(pid):
    try:
        return Indi.objects.get(pid=pid)
    except:
        return None

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

def clearDB():
    # Delete old data
    for i in Indi.objects:
        i.delete()
    for i in Fam.objects:
        i.delete()
