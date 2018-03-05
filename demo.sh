clear
echo "Begin Demo"
echo "Testing codebase"
python testing.py
echo "Upload Gedcom"
python upload.py testFam.ged
echo "Show initial database"
python query.py
echo "Checking database"
python dbCheck.py
echo "Removing Bad Data"
python fixData.py
echo "Final Output"
python query.py
