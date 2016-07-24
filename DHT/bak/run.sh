#!/bin/bash

nohup python simDHT_bwg.py > ./'log_'`date +%y-%m-%d_%H%M%S`'.log' 2>&1 &