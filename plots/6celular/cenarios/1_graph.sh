#!/bin/bash
# cd 0/
# rm -rf *.csv
# python delay.py
# python throughput.py
# python energyConsumption.py
# python lostPacketsVector.py
# python jitter.py
# cd ..

# cd 13/
# rm -rf *.csv
# python delay.py
# python throughput.py
# python energyConsumption.py
# python lostPacketsVector.py
# python jitter.py
# cd ..

# cd 26/
# rm -rf *.csv
# python delay.py
# python throughput.py
# python energyConsumption.py
# python lostPacketsVector.py
# python jitter.py
# cd ..

rm -rf *.png
rm -rf line_all.csv

python graph_delay.py
python graph_throughput.py
python graph_energyConsumption.py
python graph_lostPacketsVector.py
python graph_jitter.py
python graph_accuracy.py

exit 0