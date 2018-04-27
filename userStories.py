# fix data
from dbDef import *
from utility import *
import datetime
import collections


# US01
# takes individual
# checks if birth, marriage, divorce, and death are not in the future
# if in the future, returns true
def dateBeforeToday(x):
    today = datetime.date.today()
    if x.birth != None:
        if x.birth.date() > today: return False
    if x.death != None:
        if x.death.date() > today: return False
    for key in x.marriages:
        value = x.marriages[key]
        if value != '':
            if value.date() > today: return False
    for key in x.divorces:
        value = x.divorces[key]
        if value != '':
            if value.date() > today: return False
    return True
# US02
# takes indi
def birthBeforeMarriage(x):
    if(x.marriages == {}): return True
    for key in x.marriages:
        if x.marriages[key] != '':
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
# US04
# marriage before divorce
# takes a indi
def marriageBeforeDivorce(x):
    output = True
    for key in x.marriages:                 # every marriage
        dateM = x.marriages[key]
        if key in x.divorces:               # check for divorce
            dateD = x.divorces[key]
            if (dateM != '') and (dateD != ''): # check for dates
                output = dateM < dateD     # check dates
    return output

# US05
# Checks if an individuals own death date is not before any
# of their marrige dates
def marriageBeforeDeath(individual):
    for key in individual.marriages:
        if not individual.alive:
            if individual.marriages[key] != '':
                if individual.marriages[key] > individual.death:
                    return False
    return True

#US06
# Checks if an individuals own death date is not before any
# of their divorce dates
def divorceBeforeDeath(individual):
    if individual.death != None:
        for key in individual.divorces:
            if individual.divorces[key] > individual.death:
                return False
    return True

# US07
# Checks to make sure that a user is less than 150 years old.
def isLessThan150(indiv):
    if indiv.birth == None: return True
    now = datetime.datetime.now().date()
    age_in_days = (now - indiv.birth.date()).days
    age_in_years = age_in_days / 365
    return age_in_years < 150


#US08
# Check that child is born after the marriage of parents
def birthAfterMarriageOfParents(family):
    for cid in family.children:
        child = getIndi(pid=cid)
        if family.married != None and family.married != '':
            if child.birth.date() <= family.married.date():
                return False
            if family.divorced is not None:
                if child.birth > addMonths(family.divorced, 9):
                    return False
    return True


# US09
# Checks that each child in a family is born before the
# death of their parents
def birthBeforeDeathOfParents(family):
    isDad = False
    isMom = False
    if family.hid != '':
        dad = getIndi(family.hid)
        isDad = True
    if family.wid != '':
        mom = getIndi(family.wid)
        isMom = True
    for childId in family.children:
        child = getIndi(childId)
        if isDad:
            if(dad.death is not None):
                if(child.birth > addMonths(dad.death, 9)):
                    return False
        if isMom:
            if(mom.death is not None):
                if(child.birth > mom.death):
                    return False
    return True

# US10
# Marriage after 14
def marriageAfter14(individual):
    for key in individual.marriages:
        dom = individual.marriages[key]
        if dom != '':
            days = (dom - individual.birth).days
            if days/365 <= 14:
                return False
    return True

# US12
# takes fam and checks that the difference between the eldest child and parents
# are 60 and 80 years respectively for the wife and husband
def parentsNotTooOld(x):
    if (x.hid == '' and x.wid == ''): return True # no  parents
    if (x.children == []): return True # no children

    siblingsByAge = orderSibilingsByAge(x)
    oldestChildPid = siblingsByAge[0]
    oldestBirth = getIndi(oldestChildPid).birth

    if x.wid != '':
        wBirth = getIndi(x.wid).birth
        if wBirth != None:
            wDif = (oldestBirth - wBirth).days / 365
            if wDif >= 60: return False

    if x.hid != '':
        hBirth = getIndi(x.hid).birth
        if hBirth != None:
            hDif = (oldestBirth - hBirth).days / 365
            if hDif >= 80: return False
    return True

# US13
# takes fam
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

# US14
# No more than 5 siblings should be born at the same time
def tooManyBirthsAtOnce(family):
    if len(family.children) < 6:
        return False

    bdays = []
    for cid in family.children:
        child = getIndi(cid)
        if child != None:
            bdays.append(child.birth.date())
    counter = collections.Counter(bdays)

    if any(i > 5 for i in counter.values()):
        return True
    else:
        return False

# US15
# fewer than 15 siblings in a family
# takes a fam
# returns true if there are more than 14 siblings
def tooManySiblings(x):
    return len(x.children) >= 15


# US16
# Male last names in family
def sameMaleLastNames(family):
    child_pids = family.children
    father_pid = family.hid
    if father_pid == '': return True # no father
    father_name = getIndi(father_pid).name
    if father_name == '': return True # no father name
    lastname = father_name.split(" ")[1]
    for pid in child_pids:
        child = getIndi(pid)
        child_last_name = child.name.split(" ")[1]
        if child.gender == "M" and child_last_name != lastname:
            return False
    return True

# US17
# Parents should not marry any of their descendants
def noMarriagesToDescendants(i):
    descendants = getDescendants(i)
    spouses = getSpousePids(i)
    if any(d in spouses for d in descendants):
        return False
    return True


# US18
# siblings should not marry
# takes a fam and returns true if any siblings are married to each other
# returns true if married to sibling
def siblingMarriages(x):
    output = False
    for cid in x.children:
        child = getIndi(cid)
        for key in child.marriages:
            if key in x.children: output = True
    return output

# US21
# Husband in family should be male and wife in family should be female
def correctGenderForRole(family):
    husband = getIndi(family.hid)
    wife = getIndi(family.wid)
    if(husband == None or wife == None):
        return False
    if(husband.gender != 'M'):
        return False
    if(wife.gender != 'F'):
        return False
    return True

# US25
# Unique first names in families
def uniqueFirstNames(family):
    children = family.children
    names = []
    for cid in children:
        child = getIndi(cid)
        name = child.name.split(" ")[0]
        if name in names:
            return False
        names.append(name)
    return True

# US28
# Order siblings by age
def orderSibilingsByAge(family):
    child_objects = []
    child_ids = family.children
    for pid in child_ids:
        child_objects.append(getIndi(pid))
    sorted_array = sorted(child_objects, key=lambda i: i.birth)
    sorted_pids = []
    for child in sorted_array:
        sorted_pids.append(child.pid)

    sorted_pids = [x.encode('UTF8') for x in sorted_pids]
    return sorted_pids



# US29
# List Deceased
# returns a list of dead indis pids
def listDead():
    deadList = []
    for i in Indi.objects():
        if not i.alive: deadList.append(i.pid)
    return deadList

# US30
# list married and alive
def listMarriedAlive():
    marriedAlive = []
    for f in Fam.objects():
        if f.wid != None and f.hid != None and f.divorced == None:
            wife = getIndi(f.wid)
            husb = getIndi(f.hid)
            if(wife.alive and husb.alive):
                marriedAlive.append(f.wid)
                marriedAlive.append(f.hid)
    return marriedAlive

# US31
# list living single
def listLivingSingle():
    # go through individuals
    # check if there is a marriage that isnt in a divorce
    livingSingle = []
    for i in Indi.objects():
        single = True
        for m in i.marriages:
            if m not in i.divorces:
                single = False
        if single:
            livingSingle.append(i.pid)
    return livingSingle

# US37
# List recent survivors
#  List all living spouses and descendants of people in a GEDCOM
#  file who died in the last 30 days
def listRecentSurvivors(i):
    today = datetime.date.today()
    margin = datetime.timedelta(days = 30)
    aliveSpouses = []
    aliveDescendants = []
    spouses = []

    if i.death != None and (today-margin) <= i.death.date() <= today:
        spouses = getSpousesOfIndi(i)
        for spouse in spouses:
            if spouse.alive:
                aliveSpouses.append(spouse.pid)

        descendants = getSurvivingDescendants(i)
        if descendants:
            aliveDescendants.extend(descendants)

    return aliveSpouses, aliveDescendants


# US38
# list upcoming birthdays
# 30 days from current
def listUpcomingBirthdays():
    currentDate = datetime.datetime.now()
    birthdayList = []
    for i in Indi.objects():
        if(i.birth != None):
            b = i.birth
            x = datetime.date(currentDate.year,b.month,b.day)
            diff = x-currentDate.date()
            diff = diff.days
            if (diff >= 0 and diff <= 30):
                birthdayList.append(i.pid)
    return birthdayList
# US39
# List upcoming anniversaries
#  List all living couples in a GEDCOM file whose
#  marriage anniversaries occur in the next 30 days
def listUpcomingAnniversaries():
    today = datetime.date.today()
    margin = datetime.timedelta(days = 30)
    anniversaries = []

    for f in Fam.objects():
        if f.divorced == None and f.married != None:
            marriageDate = f.married.date()
            marriageDate = marriageDate.replace(year = today.year)
            if today <= marriageDate <= (today + margin):
                anniversaries.append(f.fid)

    return anniversaries
