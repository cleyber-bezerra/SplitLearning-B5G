#!/bin/bash
cd low/
rm -rf *.csv
python delay_low.py
python throughput_low.py
cd ..

cd medium/
rm -rf *.csv
python delay_medium.py
python throughput_medium.py
cd ..

cd high/
rm -rf *.csv
python delay_high.py
python throughput_high.py
cd ..

rm -rf *.png

python graph_delay.py
python graph_throughput.py

exit 0