# Michael Langford
# Evan Bedser

# basic imports

import sys
from prettytable import PrettyTable
import datetime
from mongoengine import *
from dbDef import *

# connect to MongoDB with pymongo
connect(DATABASE, host='localhost', port=27017)

today = datetime.date.today() # get todays date

# gedcom tags
tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR",\
        "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
# tag levels for gedcom tags
tagsLevel = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1,\
            "FAM":0, "MARR":1,"HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2,\
            "HEAD":0, "TRLR":0, "NOTE":0}

# dicts and classes will eventually be moved to mongodb

# dicts used to store finished data
indis = {} # dict of indis, format{pid:Indi}
fams = {} # dict of families, format{fid:Fam}

'''
class Indi:
    def __init__(self, pid):
        self.pid = pid # person id
        self.name = ''
        self.gender = ''
        self.birth = ''
        self.age = 0
        self.alive = True
        self.death = 'NA'
        self.child = 'NA'
        self.spouse = 'NA'
        indis[pid] = self
class Fam:
    def __init__(self, fid):
        self.fid = fid      # family id
        self.married = ''
        self.divorced = ''
        self.hid = ''       # husband id
        self.hName = ''     # husband name
        self.wid = ''       # wife id
        self.wName = ''     # wife name
        self.children = []
        fams[fid] = self
'''
class Fam:
    def __init__(self, fid):
        self.fid = fid      # family id
        self.married = ''
        self.divorced = ''
        self.hid = ''       # husband id
        self.hName = ''     # husband name
        self.wid = ''       # wife id
        self.wName = ''     # wife name
        self.children = []
        fams[fid] = self

# returns a 'Y' or 'N' to add to the standard formatting in the initial gedcom processing
def isValidLevel(level, tag):
    if level == tagsLevel[tag]:
        return 'Y'
    return 'N'

# parses file and returns a list of valid lines
def parseFile(filename):
    output = []
    with open(filename, 'r') as file:
        # initializing variables
        level = -1;
        tag = ''
        valid = ''
        args = ''
        for line in file:
            # input print
            print('--> {}'.format(line.strip()))
            # initial format of line by stripping spaces and seperating arguments
            words = line.strip().split(' ')
            level = words[0]
            tag = words[1];
            # checking tag validity and assigning variables
            if tag not in tags:
                if len(words) < 3:
                    valid = 'N'
                    args = ''
                elif words[2] in {"INDI" , "FAM"}:
                    tag = words[2]
                    args = words[1]
                    valid = isValidLevel(int(level), tag)
                else:
                    args = ' '.join(words[2:])
                    valid = 'N'
            else:
                if tag in {"INDI" , "FAM"}:
                    valid = 'N'
                    args = ' '.join(words[2:])
                else:
                    valid = isValidLevel(int(level), tag)
                    args = ' '.join(words[2:])
            # output print
            print('<-- {}|{}|{}|{}'.format(level, tag, valid, args))
            # if the tag was valid add line values to output
            if (valid == 'Y'):output.append({'level':level,'tag':tag,'args':args})
    print('---File Parsed---')
    return output

# takes the gedcom style date and converts it into the datetime format
def parseDateStr(aString):
    months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    x = aString.split(" ")
    return({"day":int(x[0]),"month":int(months.index(x[1]))+1,"year":int(x[2])})

lines = parseFile(sys.argv[1]) # parse file specified

# variable declarations
lastFam = ''
lastIndi = ''
dateType = '' # used to determine the what a date line refers to

# takes parsed lines and creates/modifies classes in dicts
for line in lines:
    # print(line) # debug line to show data in parsed format
    tag = line['tag']
    args = line['args']
    if (tag == 'INDI' and tag not in indis):
        person = Indi(pid=args)
        indis[args]=person
        lastIndi = person
        lastIndi.save()
    if (tag == 'FAM'):
        fam = Fam(args)
        lastFam = fam
    if (lastFam != ''):
        if (tag == 'MARR'):
            dateType = 'marriage'
        if (tag == 'HUSB'):
            lastFam.hid = args
        if (tag == 'WIFE'):
            lastFam.wid = args
        if (tag == 'CHIL'):
            lastFam.children.append(args)
        if (tag == 'DIV'):
            dateType = 'divorce'
        if (tag == "DATE"):
            if (dateType == 'marriage'):
                lastFam.marriage = args
            if (dateType == 'divorce'):
                lastFam.divorce = args
    if (lastIndi != ''):
        if (tag == 'NAME'):lastIndi.name = args
        if (tag == 'SEX'):lastIndi.gender = args
        if (tag == 'BIRT'): dateType = 'birth'
        if (tag == 'DEAT'): dateType = 'death'
        if (tag == 'DATE'):
            if (dateType == 'birth'):
                lastIndi.birth = args
                x = parseDateStr(args)
                age = (today - datetime.date(x['year'],x['month'],x['day'])).days
                age = int(age/365)
                lastIndi.age = age
            if (dateType == 'death'):
                lastIndi.death = args
                lastIndi.alive = False
                x = parseDateStr(args)
                y = parseDateStr(lastIndi.birth)
                age = (datetime.date(x['year'],x['month'],x['day'])- datetime.date(y['year'],y['month'],y['day'])).days
                age = int(age/365)
                lastIndi.age = age
        if (tag == "FAMC"):
            lastIndi.children.append(args)
        if (tag == "FAMS"):
            lastIndi.marriages[args] = ''
        lastIndi.save()

# populating famList with data from indiList
for i in fams:
    i = fams[i]
    i.hName = indis[i.hid].name
    i.wName = indis[i.wid].name
'''
# printing the tables from the lists
t1 = PrettyTable()
t1.field_names = ["ID","Name","Gender","Birthday","Age","Alive","Death","Child","Spouse"]
for i in indis:
    i = indis[i]
    t1.add_row([i.pid,i.name,i.gender,i.birth,i.age,i.alive,i.death,i.child,i.spouse])
print("Individuals")
print(t1)

t2 = PrettyTable()
t2.field_names = ["ID","Married","Divorced","Husband ID","Husband Name","Wife ID", "Wife Name","Children"]
for i in fams:
    i = fams[i]
    t2.add_row([i.fid,i.married,i.divorced,i.hid,i.hName,i.wid,i.wName,i.children])
print("Families")
print(t2)
'''

# for i in Indi.objects():
#   print(i.pid)
print("Data uploaded!")
