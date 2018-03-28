# family-tree
Class project for CS 555 - Agile Methodologies

Workflow:
1. upload file (see upload.py usage)
2. remove bad data (see fixData.py usage)

## Files:
### Python
dbDef.py
+ specifications of MongoDB database
+ helper funcitons to connect to MongoDB

utilities.py
+ contains useful helper functions not related to connecting to MongoDB

upload.py
+ usage "python upload.py fileName.ged (-v)(-t)"
+ uploads the information in the selected gedcom file to MongoDB
+ -v gives verbose output (shows process of upload and completion)
+ -t uses test database instead of the main one

fixData.py
+ usage "python fixData.py (-v)(-t)(-d)"
+ -v gives verbose output (shows bad records)
+ -t uses test database instead of the main one
+ -d deletes bad objects and related ids

testing.py
+ usage "python testing.py"
+ tests user stories

query.py
+ usage "python query.py (-t)"
+ -t uses test database instead of the main one
+ PrettyTable prints the contents of the database

### Bash
demo.sh
+ usage "sh demo.sh"
+ demonstrates the program by running through the tests and workflow
+ uses the test database
+ uses verbose output

### 'ged' folder
contains gedcom files
