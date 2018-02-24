# fix data
from dbDef import *
from utility import *
import datetime


# US01
# takes date and does as it says
def dateBeforeToday(x):
    return (x < datetime.datetime.now().date())

# US02
# takes indi
def birthBeforeMarriage(x):
    if(x.marriages == {}): return True
    for key in x.marriages:
        if x.birth >= x.marriages[key]:
            return False
    return True

# US03
# takes an Indi and returns true if the birth is before the death
# or if they're still alive
def birthBeforeDeath(x):
    if(x.death is not None and x.birth is not None):
        return(x.birth <= x.death)
    else:
        return(True)

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

#US08
# Check that child is born after the marriage of parents
def birthAfterMarriageOfParents(family):
    for cid in family.children:
        child = getIndi(pid=cid)
        if child.birth.date() <= family.married:
            return False
        if family.divorced is not None:
            if child.birth > addMonths(family.divorced, 9):
                return False
    return True

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
