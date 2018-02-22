# fix data
from mongoengine import *
from dbDef import *
import unittest
import datetime

connectToMongoDB()

# birth before death es05
# takes an Indi and returns true if the birth is before the death
# or if they're still alive
def birthBeforeDeath(x):
    if(x.death is not None):return(x.birth<=x.death)
    else:return(True)

# takes a fam
# mother less than 60 years older than child
# father less than 80 years older than child
# if too old return false: else true
def parentsNotTooOld(x):
    if(x.children == []): return true
    # get oldest child age
    oldestPid = ''
    oldestBirth = ''
    for childPid in x.children:
        birthDate = Indi.objects.get(pid=childPid).birth
        if(oldestBirth == ''):
            oldestBirth = birthDate
            oldestPid = childPid
        elif(birthDate < oldestBirth):
            oldestBirth = birthDate
            oldestPid = childPid
        wife = Indi.objects.get(pid=x.wid)
        husband = Indi.objects.get(pid=x.hid)
        wDif = abs((wife.birth - oldestBirth).days / 365)
        hDif = abs((husband.birth - oldestBirth).days / 365)
        if(wDif > 60 or hDif > 80): return False
        else: return True

# input datetime.date
def dateBeforeNow(x):
    return x < datetime.datetime.now().date()

# removes indis that don't pass test
for i in Fam.objects:
    print(parentsNotTooOld(i))
for i in Indi.objects:
    if(not birthBeforeDeath(i)):i.delete()


# check each family
# get the parents (wid and hid)
# get the oldest child from fam.children

class FixDataTests(unittest.TestCase):
    def test_us03(self):
        # year month day
        # dates are earliest -> latest
        # d0 is lack of date
        d1 = datetime.date(1990,1,1)             # base
        d2 = datetime.date(1990,1,2)             # later day
        d3 = datetime.date(1990,2,1)             # later month
        d4 = datetime.date(2010,1,1)             # later year
        d5 = datetime.date(2011,6,5)             # later all
        i0 = Indi(pid='test1',birth=d1)          # still alive
        i1 = Indi(pid='test2',birth=d1,death=d2) # later day
        i2 = Indi(pid='test3',birth=d1,death=d3) # later month
        i3 = Indi(pid='test4',birth=d1,death=d4) # later year
        i4 = Indi(pid='test5',birth=d1,death=d5) # later all
        i5 = Indi(pid='test2',birth=d2,death=d1) # earlier day
        i6 = Indi(pid='test3',birth=d3,death=d1) # earlier month
        i7 = Indi(pid='test4',birth=d4,death=d1) # earlier year
        i8 = Indi(pid='test5',birth=d5,death=d1) # earlier all
        i9 = Indi(pid='test',birth=d1,death=d1)  # same birth and death
        self.assertTrue(birthBeforeDeath(i0))
        self.assertTrue(birthBeforeDeath(i1))
        self.assertTrue(birthBeforeDeath(i2))
        self.assertTrue(birthBeforeDeath(i3))
        self.assertTrue(birthBeforeDeath(i4))
        self.assertFalse(birthBeforeDeath(i5))
        self.assertFalse(birthBeforeDeath(i6))
        self.assertFalse(birthBeforeDeath(i7))
        self.assertFalse(birthBeforeDeath(i8))
        self.assertTrue(birthBeforeDeath(i9))
    def test_us01(self):
        d1 = datetime.date(1990,1,1)
        d2 = datetime.date(1990,1,2)
        d3 = datetime.date(1990,2,1)
        d4 = datetime.date(2010,1,1)
        d5 = datetime.date.max
        self.assertTrue(dateBeforeNow(d1))
        self.assertTrue(dateBeforeNow(d2))
        self.assertTrue(dateBeforeNow(d3))
        self.assertTrue(dateBeforeNow(d4))
        self.assertFalse(dateBeforeNow(d5))
    if __name__ == '__main__':
        unittest.main()
