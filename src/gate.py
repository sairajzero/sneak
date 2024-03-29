"""
Automated Software Engineering - Homework Week 2
by:
    Sai Raj Thirumalai
    Sam Kwiatkowski-Martin
    Sathiya Narayanan Venkatesan

USAGE:
  python gate.py [OPTIONS]

OPTIONS:
    -c --cohen  small effect size               = .35
    -f --file   csv data file name              = ../data/auto93.csv
    -h --help   show help                       = False
    -k --k      low class frequency kludge      = 1
    -m --m      low attribute frequency kludge  = 2
    -s --seed   random number seed              = 31210
    -t --test   start up action                 = help
"""

import util as l
import test_gate as eg
import random
from the import the

def run(_the):
    if _the.help:
      print(_the.__help)
      exit(0)
    the._set(_the)
    random.seed(_the.seed)
    oops = False if eg._run(_the.test) else True

    exit(oops)

t = l.settings(__doc__)
run(l.cli(t))
