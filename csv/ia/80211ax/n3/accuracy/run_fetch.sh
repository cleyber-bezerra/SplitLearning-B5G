#!/bin/bash
python fetch_compile_sort_low.py
python fetch_compile_sort_medium.py
python fetch_compile_sort_high.py

python accuracy_low.py
python accuracy_medium.py
python accuracy_high.py

python plot_packets_res.py
exit