# fix data
from mongoengine import *
from dbDef import *
from utility import *
#from userStories import *
import unittest
import datetime

connectToMongoDB()


# US01
# takes date and does as it says
def dateBeforeToday(x):
    return (x < datetime.datetime.now().date())

# US03
# takes an Indi and returns true if the birth is before the death
# or if they're still alive
def birthBeforeDeath(x):
    if(x.death is not None and x.birth is not None):
        return(x.birth <= x.death)
    else:
        return(True)

# US02
# takes indi
def birthBeforeMarriage(x):
    if(x.marriages == {}): return True
    for key in x.marriages:
        if x.birth >= x.marriages[key]:
            return False
    return True

# US05
# Checks if an individuals own death date is not before any
# of their marrige dates
def marriageBeforeDeath(individual):
    for key in individual.marriages:
        if not individual.alive:
            if individual.marriages[key] > individual.death:
                return False
    return True

#US06
# Checks if an individuals own death date is not before any
# of their divorce dates
def divorceBeforeDeath(individual):
    for key in individual.divorces:
        if individual.divorces[key] > individual.death:
            return False
    return True

# US07
# Checks to make sure that a user is less than 150 years old.
def isLessThan150(indiv):
    now = datetime.datetime.now().date()
    age_in_days = (now - indiv.birth).days
    age_in_years = age_in_days / 365
    return age_in_years < 150

#US09
# Checks that each child in a family is born before the
# death of their parents
def birthBeforeDeathOfParents(family):
    dad = getIndi(pid=family.hid)
    mom = getIndi(pid=family.wid)
    for childId in family.children:
        child = getIndi(childId)

        if(dad.death is not None):
            if(child.birth > addMonths(dad.death, 9)):
                return False

        if(mom.death is not None):
            if(child.birth > mom.death):
                return False
    return True

# US12
# takes fam and checks that the difference between the eldest child and parents
# are 60 and 80 years respectively for the wife and husband
# def parentsNotTooOld(x):
#     if (x.children == []): return True # no children
#     oldestBirth = datetime.datetime.now()
#     for childPid in x.children:
#         cBirth = Indi.objects.get(pid=childPid).birth
#         if (cBirth < oldestBirth): oldestBirth = cBirth
#     wBirth = Indi.objects.get(pid=x.wid).birth
#     hBirth = Indi.objects.get(pid=x.hid).birth
#     wDif = (oldestBirth - wBirth).days / 365
#     hDif = (oldestBirth - hBirth).days / 365
#     return((wDif < 60)and(hDif < 80))

# US13
# takes
# more than 8 months (270 days) or less than 2 days
# true if good else false
def siblingSpacing(x):
    if(x.children == []): return True
    childrenPids = x.children
    output = True
    for pidX in childrenPids:
        for pidY in childrenPids:
            if(pidX != pidY):
                birthX = Indi.objects.get(pid=pidX).birth
                birthY = Indi.objects.get(pid=pidY).birth
                dif = abs((birthX - birthY).days)
                if(not ((dif > 270)or(dif < 2))): output = False
    return output


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

class FixDataTests(unittest.TestCase):
    def test_us01(self):
        d1 = datetime.date(1990,1,1)
        d2 = datetime.date(1990,1,2)
        d3 = datetime.date(1990,2,1)
        d4 = datetime.date(2010,1,1)
        d5 = datetime.date.max
        self.assertTrue(dateBeforeToday(d1))
        self.assertTrue(dateBeforeToday(d2))
        self.assertTrue(dateBeforeToday(d3))
        self.assertTrue(dateBeforeToday(d4))
        self.assertFalse(dateBeforeToday(d5))

    def test_us02(self):
        birthDate = datetime.date(1990,1,1)

        marriage0 = {"test0": datetime.date(1980,1,1)}      #Marriage before
        marriage1 = {"test1": datetime.date(1990,1,1)}      #Marriage same day
        marriage2 = {"test2": datetime.date(1995,1,1)}      #Marriage after death
        marriage3 = {"test3": datetime.date(1980,1,1),\
                     "test4": datetime.date(1985,1,1)}      #Two valid marriages
        marriage4 = {"test3": datetime.date(1980,1,1),\
                     "test4": datetime.date(1995,1,1)}      #One invalid marriages
        marriage5 = {}                                      #No marriages

        i0 = Indi(pid='i0', birth=birthDate, marriages=marriage0)
        i1 = Indi(pid='i1', birth=birthDate, marriages=marriage1)
        i2 = Indi(pid='i2', birth=birthDate, marriages=marriage2)
        i3 = Indi(pid='i3', birth=birthDate, marriages=marriage3)
        i4 = Indi(pid='i4', birth=birthDate, marriages=marriage4)
        i5 = Indi(pid='i5', birth=birthDate, marriages=marriage5)


        self.assertFalse(birthBeforeMarriage(i0))
        self.assertFalse(birthBeforeMarriage(i1))
        self.assertFalse(birthBeforeMarriage(i3))

        self.assertTrue(birthBeforeMarriage(i5))
        self.assertTrue(marriageBeforeDeath(i2))
        self.assertTrue(marriageBeforeDeath(i4))

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

    # Marriage before death
    def test_us05(self):
        deathDate = datetime.date(1990,1,1)

        marriage0 = {"test0": datetime.date(1980,1,1)}      #Marriage before
        marriage1 = {"test1": datetime.date(1990,1,1)}      #Marriage same day
        marriage2 = {"test2": datetime.date(1995,1,1)}      #Marriage after death
        marriage3 = {"test3": datetime.date(1980,1,1),\
                     "test4": datetime.date(1985,1,1)}      #Two valid marriages
        marriage4 = {"test3": datetime.date(1980,1,1),\
                     "test4": datetime.date(1995,1,1)}      #One invalid marriages
        marriage5 = {}                                      #No marriages

        i0 = Indi(pid='i0', death=deathDate,alive=False, marriages=marriage0)
        i1 = Indi(pid='i1', death=deathDate,alive=False, marriages=marriage1)
        i2 = Indi(pid='i2', death=deathDate,alive=False, marriages=marriage2)
        i3 = Indi(pid='i3', death=deathDate,alive=False, marriages=marriage3)
        i4 = Indi(pid='i4', death=deathDate,alive=False, marriages=marriage4)
        i5 = Indi(pid='i5', death=deathDate,alive=False, marriages=marriage5)


        self.assertTrue(marriageBeforeDeath(i0))
        self.assertTrue(marriageBeforeDeath(i1))
        self.assertTrue(marriageBeforeDeath(i3))
        self.assertTrue(marriageBeforeDeath(i5))

        self.assertFalse(marriageBeforeDeath(i2))
        self.assertFalse(marriageBeforeDeath(i4))

    # Divorce before death
    def test_us06(self):
        deathDate = datetime.date(1990,1,1)

        divorce0 = {"test0": datetime.date(1980,1,1)}      #Divroce before
        divorce1 = {"test1": datetime.date(1990,1,1)}      #Divorce same day
        divorce2 = {"test2": datetime.date(1995,1,1)}      #Divorce after death
        divorce3 = {"test3": datetime.date(1980,1,1),\
                     "test4": datetime.date(1985,1,1)}     #Two valid divorces
        divorce4 = {"test3": datetime.date(1980,1,1),\
                     "test4": datetime.date(1995,1,1)}     #One invalid divorce
        divorce5 = {}                                      #No divorces

        i0 = Indi(pid='i0', death=deathDate, divorces=divorce0)
        i1 = Indi(pid='i1', death=deathDate, divorces=divorce1)
        i2 = Indi(pid='i2', death=deathDate, divorces=divorce2)
        i3 = Indi(pid='i3', death=deathDate, divorces=divorce3)
        i4 = Indi(pid='i4', death=deathDate, divorces=divorce4)
        i5 = Indi(pid='i5', death=deathDate, divorces=divorce5)


        self.assertTrue(divorceBeforeDeath(i0))
        self.assertTrue(divorceBeforeDeath(i1))
        self.assertTrue(divorceBeforeDeath(i3))
        self.assertTrue(divorceBeforeDeath(i5))

        self.assertFalse(divorceBeforeDeath(i2))
        self.assertFalse(divorceBeforeDeath(i4))

    def test_us07(self):
        d1 = datetime.date(2050, 1, 1)
        d2 = datetime.date(2000, 1, 1)
        d3 = datetime.date(1950, 1, 1)
        d4 = datetime.date(1900, 1, 1)
        d5 = datetime.date(1850, 1, 1)
        d6 = datetime.date(1800, 1, 1)

        i1 = Indi(pid = "indi1", birth = d1)
        i2 = Indi(pid = "indi2", birth = d2)
        i3 = Indi(pid = "indi3", birth = d3)
        i4 = Indi(pid = "indi4", birth = d4)
        i5 = Indi(pid = "indi5", birth = d5)
        i6 = Indi(pid = "indi6", birth = d6)

        self.assertTrue(isLessThan150(i1))
        self.assertTrue(isLessThan150(i2))
        self.assertTrue(isLessThan150(i3))
        self.assertTrue(isLessThan150(i4))
        self.assertFalse(isLessThan150(i5))
        self.assertFalse(isLessThan150(i6))

    #TODO: Add more test cases
    def test_us09(self):
        death = datetime.date(1990,1,1)
        sonBirth = datetime.date(1990,1,1)

        mom = Indi(pid='mom', death=death)
        dad = Indi(pid='dad', death=death)
        child = Indi(pid='son', birth=sonBirth)
        family = Fam(fid='fam', hid='dad', wid='mom', children={child.pid})

        mom.save()
        dad.save()
        child.save()
        family.save()

        self.assertTrue(birthBeforeDeathOfParents(family))



if __name__ == '__main__':
    unittest.main()
