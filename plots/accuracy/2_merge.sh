#!/bin/bash
cd low
python merge_accuracy.py
mv "../result_train_sync.csv" "low_accuracy.csv"
cd..

cd medium
python merge_accuracy.py
mv "../result_train_sync.csv" "medium_accuracy.csv"
cd..

cd high
python merge_accuracy.py
mv "../result_train_sync.csv" "high_accuracy.csv"
cd..

# cd 1/
# rm -rf *.csv
# cd ..
# cd 2/
# rm -rf *.csv
# cd ..
# cd 3/
# rm -rf *.csv
# cd ..
# cd 4/
# rm -rf *.csv
# cd ..
# cd 5/
# rm -rf *.csv
# cd 6/
# rm -rf *.csv
# cd ..
# cd 7/
# rm -rf *.csv
# cd ..
# cd 8/
# rm -rf *.csv
# cd ..
# cd 9/
# rm -rf *.csv
# cd ..
# cd 10/
# rm -rf *.csv
# cd 11/
# rm -rf *.csv
# cd ..
# cd 12/
# rm -rf *.csv
# cd ..
# cd 13/
# rm -rf *.csv
# cd ..
# cd 14/
# rm -rf *.csv
# cd ..
# cd 15/
# rm -rf *.csv

source run.sh
exit 0