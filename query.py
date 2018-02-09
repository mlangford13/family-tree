from mongoengine import *
from dbDef import *
from prettytable import PrettyTable

# connect to MongoDB with pymongo
connectToMongoDB()

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
    hName = Indi.objects.get(pid=i.hid).name
    wName = Indi.objects.get(pid=i.wid).name
    t2.add_row([i.fid,i.married,i.divorced,i.hid,hName,i.wid,wName,i.children])
print("Families")
print(t2)
