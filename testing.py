from mongoengine import *
from dbDef import *
from utility import *
from userStories import *
import unittest
import datetime
import subprocess

connectToTest()

class FixDataTests(unittest.TestCase):
    def test_us01(self):
        today = datetime.datetime.today()
        past = datetime.datetime.min
        future = datetime.datetime.max
        l0 = {"a":today, "b":past, "c":''}       # good
        l1 = {"a":today, "b": past, "c": future} # bad
        l2 = {}                                  # good

        i0 = Indi(pid='i0', birth=today)    # born today
        i1 = Indi(pid='i1', birth=past)     # born past
        i2 = Indi(pid='i2', birth=future)   # born future
        i3 = Indi(pid='i3', death=today)    # death today
        i4 = Indi(pid='i4', death=past)     # death past
        i5 = Indi(pid='i5', death=future)   # death future
        i6 = Indi(pid='i6', marriages=l0)   # good
        i7 = Indi(pid='i7', marriages=l1)   # bad
        i8 = Indi(pid='i8', marriages=l2)   # good
        i9 = Indi(pid='i9', divorces=l0)    # good
        i10 = Indi(pid='i10', divorces=l1)  # bad
        i11 = Indi(pid='i11', divorces=l2)  # good

        self.assertTrue(dateBeforeToday(i0))
        self.assertTrue(dateBeforeToday(i1))
        self.assertFalse(dateBeforeToday(i2))
        self.assertTrue(dateBeforeToday(i3))
        self.assertTrue(dateBeforeToday(i4))
        self.assertFalse(dateBeforeToday(i5))
        self.assertTrue(dateBeforeToday(i6))
        self.assertFalse(dateBeforeToday(i7))
        self.assertTrue(dateBeforeToday(i8))
        self.assertTrue(dateBeforeToday(i9))
        self.assertFalse(dateBeforeToday(i10))
        self.assertTrue(dateBeforeToday(i11))

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
        marriage6 = {"test3": datetime.date(1980,1,1),\
                     "test4": ''}                             #Two valid marriages

        i0 = Indi(pid='i0', birth=birthDate, marriages=marriage0)
        i1 = Indi(pid='i1', birth=birthDate, marriages=marriage1)
        i2 = Indi(pid='i2', birth=birthDate, marriages=marriage2)
        i3 = Indi(pid='i3', birth=birthDate, marriages=marriage3)
        i4 = Indi(pid='i4', birth=birthDate, marriages=marriage4)
        i5 = Indi(pid='i5', birth=birthDate, marriages=marriage5)
        i6 = Indi(pid='i6', birth=birthDate, marriages=marriage6)


        self.assertFalse(birthBeforeMarriage(i0))
        self.assertFalse(birthBeforeMarriage(i1))
        self.assertFalse(birthBeforeMarriage(i3))

        self.assertTrue(birthBeforeMarriage(i5))
        self.assertTrue(marriageBeforeDeath(i2))
        self.assertTrue(marriageBeforeDeath(i4))
        self.assertTrue(marriageBeforeDeath(i6))

    def test_us03(self):
        # year month day
        # dates are earliest -> latest
        # d0 is lack of date
        d1 = datetime.datetime(1990,1,1)             # base
        d2 = datetime.datetime(1990,1,2)             # later day
        d3 = datetime.datetime(1990,2,1)             # later month
        d4 = datetime.datetime(2010,1,1)             # later year
        d5 = datetime.datetime(2011,6,5)             # later all
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
    # Marriage before divorce
    def test_us04(self):
        m0 = {"test0": datetime.date(1980,1,1)}      # Marriage before
        d0 = {"test0": datetime.date(1981,2,2)}

        m1 = {"test0": datetime.date(1980,1,1)}      # Divorce Before
        d1 = {"test0": datetime.date(1929,2,2)}

        m2 = {"test0": datetime.date(1980,1,1)}      # Same day
        d2 = {"test0": datetime.date(1980,1,1)}

        m3 = {}                                      # No marriages
        d3 = {"test0": datetime.date(1981,2,2)}

        m4 = {"test0": datetime.date(1980,1,1)}      # No divorces
        d4 = {}

        m5 = {}                                      # No marriages or divorces
        d5 = {}

        m6 = {"test0": datetime.date(1980,1,1),\
                "test1": datetime.date(1985,1,1),\
                "test2": datetime.date(1990,1,1)}    # Multiple valid
        d6 = {"test0": datetime.date(1984,2,2),\
                "test1": datetime.date(1987,2,2)}

        m7 = {"test0": datetime.date(1980,1,1),\
                "test1": datetime.date(1985,1,1),\
                "test2": datetime.date(1990,1,1)}    # One invalid
        d7 = {"test0": datetime.date(1984,2,2),\
                "test1": datetime.date(1987,2,2),\
                "test2": datetime.date(1983,2,2)}

        m8 = {"test0": datetime.date(1980,1,1),\
                "test1": datetime.date(1985,1,1),\
                "test2": datetime.date(1990,1,1)}    # All invalid
        d8 = {"test0": datetime.date(1950,2,2),\
                "test1": datetime.date(1967,2,2),\
                "test2": datetime.date(1981,2,2)}

        i0 = Indi(pid='i0', marriages=m0,divorces=d0)
        i1 = Indi(pid='i1', marriages=m1,divorces=d1)
        i2 = Indi(pid='i2', marriages=m2,divorces=d2)
        i3 = Indi(pid='i3', marriages=m3,divorces=d3)
        i4 = Indi(pid='i4', marriages=m4,divorces=d4)
        i5 = Indi(pid='i5', marriages=m5,divorces=d5)
        i6 = Indi(pid='i6', marriages=m6,divorces=d6)
        i7 = Indi(pid='i7', marriages=m7,divorces=d7)
        i8 = Indi(pid='i8', marriages=m8,divorces=d8)

        self.assertTrue(marriageBeforeDivorce(i0))
        self.assertFalse(marriageBeforeDivorce(i1))
        self.assertFalse(marriageBeforeDivorce(i2))
        self.assertTrue(marriageBeforeDivorce(i3))
        self.assertTrue(marriageBeforeDivorce(i4))
        self.assertTrue(marriageBeforeDivorce(i5))
        self.assertTrue(marriageBeforeDivorce(i6))
        self.assertFalse(marriageBeforeDivorce(i7))
        self.assertFalse(marriageBeforeDivorce(i8))

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
        marriage6 = {"test3": datetime.date(1980,1,1),\
                     "test4": ''}                           #Two valid marriages

        i0 = Indi(pid='i0', death=deathDate,alive=False, marriages=marriage0)
        i1 = Indi(pid='i1', death=deathDate,alive=False, marriages=marriage1)
        i2 = Indi(pid='i2', death=deathDate,alive=False, marriages=marriage2)
        i3 = Indi(pid='i3', death=deathDate,alive=False, marriages=marriage3)
        i4 = Indi(pid='i4', death=deathDate,alive=False, marriages=marriage4)
        i5 = Indi(pid='i5', death=deathDate,alive=False, marriages=marriage5)
        i6 = Indi(pid='i6', death=deathDate,alive=False, marriages=marriage6)


        self.assertTrue(marriageBeforeDeath(i0))
        self.assertTrue(marriageBeforeDeath(i1))
        self.assertTrue(marriageBeforeDeath(i3))
        self.assertTrue(marriageBeforeDeath(i5))
        self.assertTrue(marriageBeforeDeath(i6))

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
        d1 = datetime.datetime(2050, 1, 1)
        d2 = datetime.datetime(2000, 1, 1)
        d3 = datetime.datetime(1950, 1, 1)
        d4 = datetime.datetime(1900, 1, 1)
        d5 = datetime.datetime(1850, 1, 1)
        d6 = datetime.datetime(1800, 1, 1)

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

    def test_us08(self):
        c1Birth = datetime.datetime(1990,1,1)
        c2Birth = datetime.datetime(1995,1,1)
        c3Birth = datetime.datetime(2000,1,1)
        c4Birth = datetime.datetime(2005,1,1)
        c5Birth = datetime.datetime(2010,8,1)
        c6Birth = datetime.datetime(2010,11,1)
        c1 = Indi(pid='c1', name='c1',birth = c1Birth)
        c2 = Indi(pid='c2', name='c2',birth = c2Birth)
        c3 = Indi(pid='c3', name='c3',birth = c3Birth)
        c4 = Indi(pid='c4', name='c4',birth = c4Birth)
        c5 = Indi(pid='c5', name='c5',birth = c5Birth)
        c6 = Indi(pid='c6', name='c6',birth = c6Birth)

        #children = {c1.pid, c2.pid, c3.pid, c4.pid}

        marriage1 = datetime.datetime(1995,1,1)
        fam1 = Fam(fid='fam1', married=marriage1, children={c1.pid})
        fam2 = Fam(fid='fam2', married=marriage1, children={c2.pid})
        fam3 = Fam(fid='fam3', married=marriage1, children={c3.pid})
        fam4 = Fam(fid='fam4', married=marriage1, children={c4.pid})
        fam5 = Fam(fid='fam5', married=marriage1)

        divorce = datetime.datetime(2010,1,1)
        fam6 = Fam(fid='fam6', married=marriage1, divorced=divorce, children={c5.pid})
        fam7 = Fam(fid='fam7', married=marriage1, divorced=divorce, children={c6.pid})

        for obj in [c1, c2, c3, c4, c5, c6, fam1, fam2, fam3, fam4, fam5, fam6, fam7]:
            obj.save()

        self.assertFalse(birthAfterMarriageOfParents(fam1))
        self.assertFalse(birthAfterMarriageOfParents(fam2))
        self.assertTrue(birthAfterMarriageOfParents(fam3))
        self.assertTrue(birthAfterMarriageOfParents(fam4))
        self.assertTrue(birthAfterMarriageOfParents(fam5))

        self.assertTrue(birthAfterMarriageOfParents(fam6))
        self.assertFalse(birthAfterMarriageOfParents(fam7))


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

    def test_us10(self):
        bday = datetime.datetime(1980,1,1)

        m1date = datetime.datetime(1980, 1, 1)
        m2date = datetime.datetime(1990, 1, 1)
        m3date = datetime.datetime(1995, 1, 1)
        m4date = datetime.datetime(2000, 1, 1)

        i1 = Indi(pid = "i1", birth = bday)                              # True
        i2 = Indi(pid = "i2", birth = bday, marriages = {"i0" : m1date}) # False
        i3 = Indi(pid = "i3", birth = bday, marriages = {"i0" : m2date}) # False
        i4 = Indi(pid = "i4", birth = bday, marriages = {"i0" : m3date, "i1": m4date}) # True
        i5 = Indi(pid = "i5", birth = bday, marriages = {"i0" : m2date, "i1": m4date}) # False

        for obj in [i1, i2, i3, i4, i5]:
            obj.save()

        self.assertTrue(marriageAfter14(i1))
        self.assertFalse(marriageAfter14(i2))
        self.assertFalse(marriageAfter14(i3))
        self.assertTrue(marriageAfter14(i4))
        self.assertFalse(marriageAfter14(i5))

    # parents not too old
    def test_us12(self):
        y = 365
        d0 = datetime.date(2000,1,1) # child date (older)
        d1 = d0 + datetime.timedelta(days = 200) # child date (younger)
        d2 = d0 - datetime.timedelta(days = 79*y) # young enough father
        d3 = d0 - datetime.timedelta(days = 80*y) # too old father
        d4 = d0 - datetime.timedelta(days = 81*y) # too old father
        d5 = d0 - datetime.timedelta(days = 59*y) # young enough mother
        d6 = d0 - datetime.timedelta(days = 60*y) # too old mother
        d7 = d0 - datetime.timedelta(days = 61*y) # too old mother

        c0 = Indi(pid='c0',birth=d0)
        c1 = Indi(pid='c1',birth=d1)

        cl0 = []
        cl1 = ['c0']
        cl2 = ['c0','c1']

        h0 = Indi(pid='h0',birth=d2)
        h1 = Indi(pid='h1',birth=d3)
        h2 = Indi(pid='h2',birth=d4)

        w0 = Indi(pid='w0',birth=d5)
        w1 = Indi(pid='w1',birth=d6)
        w2 = Indi(pid='w2',birth=d7)

        f0 = Fam(fid='f0',hid='h0',wid='w0',children=cl0) # no children
        f1 = Fam(fid='f1',hid='h0',wid='w0',children=cl1) # one child
        f2 = Fam(fid='f2',hid='h0',wid='w0',children=cl2) # less mother
        f3 = Fam(fid='f3',hid='h0',wid='w1',children=cl2) # equal mother
        f4 = Fam(fid='f4',hid='h0',wid='w2',children=cl2) # more mother
        f5 = Fam(fid='f5',hid='h0',wid='w0',children=cl2) # less father
        f6 = Fam(fid='f6',hid='h1',wid='w0',children=cl2) # equal father
        f7 = Fam(fid='f7',hid='h2',wid='w0',children=cl2) # more father
        f8 = Fam(fid='f8',hid='h2',wid='w2',children=cl2) # both more

        saveList = [c0,c1,h0,h1,h2,w0,w1,w2,f0,f1,f2,f3,f4,f5,f6,f7,f8]

        clearDB()
        for i in saveList:
            i.save()

        self.assertTrue(parentsNotTooOld(f0))
        self.assertTrue(parentsNotTooOld(f1))
        self.assertTrue(parentsNotTooOld(f2))
        self.assertFalse(parentsNotTooOld(f3))
        self.assertFalse(parentsNotTooOld(f4))
        self.assertTrue(parentsNotTooOld(f5))
        self.assertFalse(parentsNotTooOld(f6))
        self.assertFalse(parentsNotTooOld(f7))
        self.assertFalse(parentsNotTooOld(f8))
        clearDB()

    # sibling spacing
    def test_us13(self):
        d0 = datetime.date(2000,1,1)
        d1 = d0 + datetime.timedelta(days = 271)
        d2 = d0 + datetime.timedelta(days = 270)
        d3 = d0 + datetime.timedelta(days = 2)
        d4 = d0 + datetime.timedelta(days = 1)
        d5 = d0 + datetime.timedelta(days = 0)

        i0 = Indi(pid='i0', birth=d0)
        i1 = Indi(pid='i1', birth=d1)
        i2 = Indi(pid='i2', birth=d2)
        i3 = Indi(pid='i3', birth=d3)
        i4 = Indi(pid='i4', birth=d4)
        i5 = Indi(pid='i5', birth=d5)
        iList = [i0,i1,i2,i3,i4,i5]

        f1 = Fam(fid='f1',children=['i0','i1']) # > 270 days
        f2 = Fam(fid='f2',children=['i0','i2']) # = 270 days
        f3 = Fam(fid='f3',children=['i0','i3']) # = 2 days
        f4 = Fam(fid='f4',children=['i0','i4']) # < 2 days
        f5 = Fam(fid='f5',children=['i0','i5']) # same day
        fList = [f1,f2,f3,f4,f5]

        clearDB()
        for i in iList:
            i.save()
        for f in fList:
            f.save()
        self.assertTrue(siblingSpacing(f1))
        self.assertFalse(siblingSpacing(f2))
        self.assertFalse(siblingSpacing(f3))
        self.assertTrue(siblingSpacing(f4))
        self.assertTrue(siblingSpacing(f5))
        clearDB()

    # No more than 5 siblings should be born at the same time
    def test_us14(self):
        birth_SAME = datetime.date(2000,1,1)
        birth_DIF6 = datetime.date(2001,1,1)
        c0_SAME = Indi(pid='c0', birth=birth_SAME)
        c1_SAME = Indi(pid='c1', birth=birth_SAME)
        c2_SAME = Indi(pid='c2', birth=birth_SAME)
        c3_SAME = Indi(pid='c3', birth=birth_SAME)
        c4_SAME = Indi(pid='c4', birth=birth_SAME)
        c5_SAME = Indi(pid='c5', birth=birth_SAME)
        c6_DIF = Indi(pid='c6', birth=birth_DIF6)

        f0 = Fam(fid='f0', children=['c0','c1','c2','c3','c4','c5','c6'])
        f1 = Fam(fid='f1', children=['c0','c1','c2','c3','c4','c6'])
        f2 = Fam(fid='f2')
        f3 = Fam(fid='f0', children=['c0','c1','c2','c6','c3','c4','c5'])

        saveList = [c0_SAME, c1_SAME, c2_SAME, c3_SAME, c4_SAME, c5_SAME, c6_DIF]

        clearDB()
        for obj in saveList:
            obj.save()
        self.assertTrue(tooManyBirthsAtOnce(f0))
        self.assertTrue(tooManyBirthsAtOnce(f3))
        self.assertFalse(tooManySiblings(f1))
        self.assertFalse(tooManySiblings(f2))
        clearDB()

    def test_us15(self):
        c0 = []
        c1 = ['testId']*14
        c2 = ['testId']*15
        c3 = ['testId']*16

        f0 = Fam(fid='f0',children=c0)
        f1 = Fam(fid='f1',children=c1)
        f2 = Fam(fid='f2',children=c2)
        f3 = Fam(fid='f3',children=c3)

        self.assertFalse(tooManySiblings(f0))
        self.assertFalse(tooManySiblings(f1))
        self.assertTrue(tooManySiblings(f2))
        self.assertTrue(tooManySiblings(f3))




    def test_us16(self):
        i1 = Indi(pid = "i1", gender = "M", name = "Harry Potter")
        i2 = Indi(pid = "i2", gender = "M", name = "James Potter")
        i3 = Indi(pid = "i3", gender = "F", name = "Lilly Evans")
        i4 = Indi(pid = "14", gender = "M", name = "Albus Dumbledore")

        fam1 = Fam(fid = "fam1", hid = i2.pid, children={i1.pid}) #True
        fam2 = Fam(fid = "fam2", hid = i2.pid, children={i1.pid, i3.pid}) #True
        fam3 = Fam(fid = "fam3", hid = i4.pid, children={i1.pid, i2.pid}) #False
        fam4 = Fam(fid = "fam4", hid = i1.pid) #True
        fam5 = Fam(fid = "fam5", wid = i3.pid, hid = i2.pid, children = {i1.pid})

        for obj in [i1, i2, i3, i4, fam1, fam2, fam3, fam4, fam5]:
            obj.save()

        self.assertTrue(sameMaleLastNames(fam1))
        self.assertTrue(sameMaleLastNames(fam2))
        self.assertFalse(sameMaleLastNames(fam3))
        self.assertTrue(sameMaleLastNames(fam4))
        self.assertTrue(sameMaleLastNames(fam5))

    def test_us18(self):
        i0 = Indi(pid='i0', marriages={'i1':''})  # fam
        i1 = Indi(pid='i1', marriages={'i0':''})  # fam
        i2 = Indi(pid='i2', marriages ={'i3':''}) # fam
        i3 = Indi(pid='i3', marriages={'i2':''})  # not fam

        f0 = Fam(fid='f0',children=[])            # good
        f1 = Fam(fid='f1',children=['i0'])        # good
        f2 = Fam(fid='f2',children=['i0','i1'])   # bad
        f3 = Fam(fid='f3',children=['i2'])        # good

        saveList = [i0,i1,i2,i3,f0,f1,f2,f3]

        clearDB()
        for i in saveList: i.save()
        self.assertFalse(siblingMarriages(f0))
        self.assertFalse(siblingMarriages(f1))
        self.assertTrue(siblingMarriages(f2))
        self.assertFalse(siblingMarriages(f3))
        clearDB()

    def test_us21(self):
        dad_M = Indi(pid='dad_M', gender='M')
        dad_F = Indi(pid='dad_F', gender='F')
        dad_NA = Indi(pid='dad_NA')

        mom_F = Indi(pid='mom_F', gender='F')
        mom_M = Indi(pid='mom_M', gender='M')
        mom_NA = Indi(pid='mom_NA')

        f0 = Fam(fid='valid', hid = dad_M.pid , wid = mom_F.pid)
        f1 = Fam(fid='invalid_dad', hid = dad_F.pid , wid = mom_F.pid)
        f2 = Fam(fid='invalid_mom', hid = dad_M.pid , wid = mom_M.pid)
        f3 = Fam(fid='invalid_both', hid = dad_F.pid , wid = mom_M.pid)
        f4 = Fam(fid='invalid_mom_NA', hid = dad_M.pid, wid = mom_NA.pid)
        f5 = Fam(fid='invalid_dad_NA', hid = dad_NA.pid, wid = mom_F.pid)
        f6 = Fam(fid='invalid_both_NA', hid = dad_NA.pid, wid = mom_NA.pid)
        f7 = Fam(fid='invalid_dont_exist_dad', hid='dont_exist', wid = mom_F.pid)
        f8 = Fam(fid='invalid_dont_exist_mom', hid= dad_M.pid, wid='dont_exist')
        f9 = Fam(fid='invalid_dont_exist_dad', hid='dont_exist', wid='dont_exist')

        saveList = [dad_M, dad_F, dad_NA, mom_F, mom_M, mom_NA]

        clearDB()
        for i in saveList:
            i.save()
        self.assertTrue(correctGenderForRole(f0))
        self.assertFalse(correctGenderForRole(f1))
        self.assertFalse(correctGenderForRole(f2))
        self.assertFalse(correctGenderForRole(f3))
        self.assertFalse(correctGenderForRole(f4))
        self.assertFalse(correctGenderForRole(f5))
        self.assertFalse(correctGenderForRole(f6))
        self.assertFalse(correctGenderForRole(f7))
        self.assertFalse(correctGenderForRole(f8))
        self.assertFalse(correctGenderForRole(f9))
        clearDB()


    def test_us25(self):
        i1 = Indi(pid="john1", name="John")
        i2 = Indi(pid="john2", name="John")
        i3 = Indi(pid="amy", name="Amy")
        i4 = Indi(pid="sue", name="Sue")
        i5 = Indi(pid="greg1", name="Greg")
        i6 = Indi(pid="greg2", name="Greg")

        fam1 = Fam(fid="fam1", children={i1.pid, i3.pid, i4.pid}) #John, Amy, Sue
        fam2 = Fam(fid="fam2", children={i2.pid, i4.pid, i6.pid})#John, Sue, Greg
        fam3 = Fam(fid="fam3", children={i1.pid, i2.pid, i6.pid})#John,John, Greg
        fam4 = Fam(fid="fam4", children={i3.pid, i5.pid, i6.pid})#Amy, Greg, Greg
        fam5 = Fam(fid="fam5", children={i5.pid, i6.pid}) #Greg, Greg
        fam6 = Fam(fid="fam6")
        fam7 = Fam(fid="fam7", children={i1.pid}) #John

        for obj in [i1, i2, i3, i4, i5, i6, fam1, fam2, fam3, fam4, fam5, fam6, fam7]:
            obj.save()

        self.assertTrue(uniqueFirstNames(fam1))
        self.assertTrue(uniqueFirstNames(fam2))
        self.assertFalse(uniqueFirstNames(fam3))
        self.assertFalse(uniqueFirstNames(fam4))
        self.assertFalse(uniqueFirstNames(fam5))
        self.assertTrue(uniqueFirstNames(fam6))
        self.assertTrue(uniqueFirstNames(fam7))

    def test_us29(self):
        i0 = Indi(pid="i0",alive=True)
        i1 = Indi(pid="i1",alive=False)
        i2 = Indi(pid="i2",alive=False)

        clearDB()

        self.assertTrue(listDead() == [])

        i0.save()
        self.assertTrue(listDead() == [])

        i1.save()
        self.assertTrue(listDead() == ["i1"])

        i2.save()
        self.assertTrue(listDead() == ["i1","i2"])

        clearDB()



if __name__ == '__main__':
    unittest.main()
