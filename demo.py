# demonstration
import subprocess

print("DEMO")

print("Testing Codebase")
print(subprocess.check_output(['python','testing.py']))

print("Uploading File")
subprocess.run(['python','upload.py','myFamily.ged'])
print("File Uploaded")

print("Checking File")
print(subprocess.check_output(['python','dbCheck.py']))
print("File Checked")

print("Demo Complete")
