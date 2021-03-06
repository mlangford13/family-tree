clear

echo "------------------------------"
echo "--- Begin Demo ---"
echo "------------------------------"
echo ""
echo "------------------------------"
echo "---Testing codebase ---"
echo "------------------------------"
python testing.py
echo "------------------------------"
echo "---Running Precheck---"
echo "------------------------------"
python precheck.py ged/US04_08.ged
echo ""
echo "------------------------------"
echo "--- Uploading gedcom file---"
echo "------------------------------"
python upload.py ged/US04_08.ged -t
echo ""
echo "-----------------------------------"
echo "--- Showing initial database ---"
echo "-----------------------------------"
python query.py -t
echo ""
echo "-----------------------------------------------------"
echo "--- Checking database and removing bad data ---"
echo "-----------------------------------------------------"
python fixData.py -t -v -d
echo ""
echo "-------------------------------------------------------------"
echo "--- Checking the database to show no bad data remains ---"
echo "-------------------------------------------------------------"
python fixData.py -t -v
echo ""
echo "------------------------------"
echo "--- Final Output ---"
echo "------------------------------"
python query.py -t
