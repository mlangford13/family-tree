# Michael Langford
# Evan Bedser

# basic imports

import sys
from prettytable import PrettyTable
import datetime
from mongoengine import *
from dbDef import *

# connect to MongoDB with pymongo
connectToMongoDB()

today = datetime.date.today() # get todays date

# gedcom tags
tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR",\
        "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
# tag levels for gedcom tags
tagsLevel = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1,\
            "FAM":0, "MARR":1,"HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2,\
            "HEAD":0, "TRLR":0, "NOTE":0}


# dicts used to store finished data
indis = {} # dict of indis, format{pid:Indi}
fams = {} # dict of families, format{fid:Fam}

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
        fam = Fam(fid=args)
        fams[args]=fam
        lastFam = fam
        lastFam.save()
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
        lastFam.save()
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

# add families and marriages to indi records
# TODO : add divorces
for i in fams:
    i = fams[i]
    husband = Indi.objects.get(pid=i.hid)
    if i.fid not in husband.families: husband.families.append(i.fid)
    husband.marriages[i.wid]=i.married
    husband.save()

    wife = Indi.objects.get(pid=i.wid)
    if i.fid not in wife.families: wife.families.append(i.fid)
    wife.marriages[i.hid]=i.married
    wife.save()

    for cid in i.children:
        child = Indi.objects(pid=cid)[0]
        if i.fid not in child.families: child.families.append(i.fid)
        child.save()

print("Data uploaded!")
