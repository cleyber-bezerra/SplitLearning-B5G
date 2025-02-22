#!/bin/bash
#../../ns3 clean
../../ns3 configure
../../ns3 build
../../ns3 run scratch/SplitLearning-B5G/cttc-nr-split.cc
exit