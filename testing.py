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

if __name__ == '__main__':
    unittest.main()
