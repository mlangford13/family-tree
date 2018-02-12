# fix data
from mongoengine import *
from dbDef import *

connectToMongoDB()

# birth before death es05
# takes an Indi and returns true if the birth is before the death
# or if they're still alive
def birthBeforeDeath(x):
    if(x.death is not None):return(i.birth<i.death)
    else:return(True)

for i in Indi.objects:
    print(birthBeforeDeath(i))
