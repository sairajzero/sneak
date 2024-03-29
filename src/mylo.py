"""

Automated Software Engineering - Homework Week 5
by:
    Sai Raj Thirumalai
    Sam Kwiatkowski-Martin
    Sathiya Narayanan Venkatesan

USAGE:
  python mylo.py [OPTIONS]

OPTIONS:
    -b --bins   max number of bins              = 16
    -B --Beam   max number of ranges            = 10
    -c --cohen  small effect size               = .35
    -C --Cut    ignore ranges less than C*max   = .1
    -d --d      frist cut                       = 32
    -D --D      second cut                      = 4
    -f --file   csv data file name              = ../data/diabetes.csv
    -F --Far    how far to search for faraway?  = .95
    -h --help   show help                       = False
    -H --Half   #items to use in clustering     = 256
    -p --p      weights for distance            = 2
    -s --seed   random number seed              = 31210
    -S --Support coeffecient on best            = 2
    -t --todo   start up action                 = help

"""

import util as l
import test_mylo as eg
import random
from the import the

def run(_the):
    if _the.help:
      print(_the.__help)
      exit(0)
    the._set(_the)
    random.seed(_the.seed)
    oops = False if eg._run(_the.todo) else True

    exit(oops)

t = l.settings(__doc__)
run(l.cli(t))
