from mongoengine import *
from dbDef import *
from prettytable import PrettyTable
from utility import *
from userStories import *
import argparse

parser = argparse.ArgumentParser(description='PrettyTable prints database.')
parser.add_argument('-t',action='store_true',help='Use the test database.')
args = parser.parse_args()
test = args.t

if test:
    connectToTest()
    print("Connected to Test Database")
else:
    connectToMongoDB()
    print("Connected to Main Database")

# printing the tables from the lists
t1 = PrettyTable()
t1.field_names = ["ID","Name","Gender","Birthday","Age","Alive","Death","Child","Spouse"]
for i in Indi.objects:
    t1.add_row([i.pid,i.name,i.gender,i.birth,i.age,i.alive,i.death,i.children,i.marriages])
print("Individuals")
print(t1)

t2 = PrettyTable()
t2.field_names = ["ID","Married","Divorced","Husband ID","Husband Name","Wife ID", "Wife Name","Children"]
for i in Fam.objects:
    hName = ''
    wName = ''
    if i.hid != '' : hName = getIndi(i.hid).name
    if i.wid != '' : wName = getIndi(i.wid).name
    t2.add_row([i.fid,i.married,i.divorced,i.hid,hName,i.wid,wName,i.children])
print("Families")
print(t2)

# US29 List deceased
print("Deceased: " + str(listDead()))

# US30 List Married and Alive
print("Married and Alive: " + str(listMarriedAlive()))

# US31 List Single and Alive
print("Single and Alive: " + str(listLivingSingle()))


# US37 List recent survivors
for i in Indi.objects():
    spouses, descendants = listRecentSurvivors(i)
    if spouses or descendants: print("Individual "+ i.pid +" survived by:")
    if spouses: print("\tSpouses: " + str(spouses))
    if descendants: print("\tDescendants: " + str(descendants))

# US38 List Upcoming Birthdays
print("Upcoming Birthdays: " + str(listUpcomingBirthdays()))

# US39
print("Upcoming Anniversaries: ")
anniversaries = getFams(listUpcomingAnniversaries())
for f in anniversaries:
    print("\tHusband: " + f.hid + ", Wife: " + f.wid + ", Married: " + str(f.married))
