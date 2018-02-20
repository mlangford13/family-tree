from mongoengine import *
from dbDef import *
import datetime
import calendar

def getIndi(pid):
    return Indi.objects.get(pid=pid)

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
