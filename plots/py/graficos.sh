#!/bin/bash

mv ../*.csv ../csv/

python barra_delay.py
python barra_energy.py
python barra_loss.py
python barra_throughput.py

python line_delay.py
python line_energy.py
python line_loss.py
python line_throughput.py
python line_all.py

exit 0