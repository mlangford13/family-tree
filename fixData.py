# fix data
from mongoengine import *
from dbDef import *
import unittest
import datetime

connectToMongoDB()

# birth before death us03
# takes an Indi and returns true if the birth is before the death
# or if they're still alive
def birthBeforeDeath(x):
    if(x.death is not None):return(x.birth<=x.death)
    else:return(True)
#
def marriageBeforeDeath(individual):
    for marriage in individual.marriages:
        if marriage.value > individual.death:
            return False
    return True

# removes indis that don't pass test
for i in Indi.objects:
    if(not birthBeforeDeath(i)):i.delete()

class MyTests(unittest.TestCase):
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
        print("Hello")
        death0 = datetime.date(1990,1,1)        #base
        #death1 = datetime.date(1990,)

        marriage0 = datetime.date(1980,1,1)
        i0 = Indi(pid='i0', death=death0, marriages={"test0", marriage0})
        self.assertTrue(marriageBeforeDeath(i0))

    if __name__ == '__main__':
        unittest.main()
