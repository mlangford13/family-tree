clear
echo "--- Begin Demo ---"
echo "---Testing codebase ---"
python testing.py
echo "--- Uploading gedcom file---"
python upload.py ged/testFam.ged -t
echo "--- Showing initial database ---"
python query.py -t
echo "--- Checking database and removing bad data ---"
python fixData.py -t -v -d
echo "--- Checking the database to show no bad data remains ---"
python fixData.py -t -v
echo "--- Final Output ---"
python query.py -t
