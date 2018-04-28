

import sys
from prettytable import PrettyTable
import datetime
from mongoengine import *
from dbDef import *
import argparse

parser = argparse.ArgumentParser(description='Uploads gedcom file to database.')
parser.add_argument('-v',action='store_true',help='Verbose output.')
parser.add_argument('fileName', metavar='F',type=str,help='Gedcom file to be uploaded.')
args = parser.parse_args()

debug = args.v
fileName = args.fileName

today = datetime.date.today() # get todays date

# gedcom tags
tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR",\
        "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]
# tag levels for gedcom tags
tagsLevel = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1,\
            "FAM":0, "MARR":1,"HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2,\
            "HEAD":0, "TRLR":0, "NOTE":0}


# parses file and checks for duplicate ids or 
def preCheckFile(filename):
    valid = True
    pidList = []
    fidList = []
    with open(filename, 'r') as file:
        for line in file:
            # initial format of line by stripping spaces and seperating arguments
            words = line.strip().split(' ')
            level = words[0]
            level = int(level)
            args = words[2:]
            #print(level)
            #print(tag)
            #print(words)
            if len(words) >= 3:
                if words[2] == "INDI" and level == 0:
                    id = words[1]
                    if id not in pidList:
                        pidList.append(id)
                        if debug: print("Indi Id not a duplicate")
                    else:
                        valid = False
                        errorMessage = "Indi Id "+id+" is duplicated"
                        print(errorMessage)
                if words[2] == "FAM" and level == 0:
                    id = words[1]
                    if id not in fidList:
                        fidList.append(id)
                        if debug: print("Family Id not a duplicate")
                    else:
                        valid = False
                        errorMessage = "Familt Id "+id+" is duplicated"
                        print(errorMessage)
            if words[1] == "DATE":
                if len(args) != 3: throw("Date does not have required fields")
                months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
                # format day month year
                day = args[0]
                month = args[1]
                year = args[2]

                if month not in months:
                    valid = False
                    print("Month "+month+" does not exist")
                else:
                    month = months.index(month)+1
                    day = int(day)
                    year = int(year)
                    month = int(month)
                    try:
                        testDate = datetime.datetime(year,month,day)
                        if debug: print("Valid Date")
                    except ValueError:
                        valid = False
                        print("Date "+str(args)+" is invalid")
        return valid

x = preCheckFile(fileName)
if(x):print("Precheck successful. The file is ready for upload.")
else:print("Precheck failed. The file will cause errors on upload")
