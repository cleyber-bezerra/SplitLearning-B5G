#!/bin/bash
cd low/
rm -rf *.csv
python delay_low.py
python throughput_low.py
python energyConsumption.py
python lostPacketsVector.py
python jitter.py
python line_all.py
cd ..

cd medium/
rm -rf *.csv
python delay_medium.py
python throughput_medium.py
python energyConsumption.py
python lostPacketsVector.py
python jitter.py
python line_all.py
cd ..

cd high/
rm -rf *.csv
python delay_high.py
python throughput_high.py
python energyConsumption.py
python lostPacketsVector.py
python jitter.py
python line_all.py
cd ..

rm -rf *.png
rm -rf line_all.csv

python graph_delay.py
python graph_throughput.py
python graph_energyConsumption.py
python graph_lostPacketsVector.py
python graph_jitter.py
python line_all.py
python graph_line_all.py

exit 0