# Automated Software Engineering - Homework
![Python](https://img.shields.io/badge/python-v3.10+-brightgreen.svg)
![Lines of code](https://tokei.rs/b1/github/ase-spring24-team/hw1)

## Quick Guide
To run use the following commands:
```
cd src
```
#### `gate.py`
Usage: 
```
python gate.py [OPTIONS]
```

Options:
```
    -c --cohen  small effect size               = .35
    -f --file   csv data file name              = ../data/auto93.csv
    -h --help   show help                       = False
    -k --k      low class frequency kludge      = 1
    -m --m      low attribute frequency kludge  = 2
    -s --seed   random number seed              = 31210
    -t --test   start up action                 = help
```
To view help:
```
python gate.py -h
```
To list all available tests:
```
python gate.py -t egs
```
To run all tests:
```
python gate.py -t all
```
#### `mylo.py`
Usage: 
```
python mylo.py [OPTIONS]
```

Options:
```
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
```
To view help:
```
python mylo.py -h
```
To list all available tests:
```
python mylo.py -t egs
```
To run all tests:
```
python mylo.py -t all
```


## Homework Tasks
### HW2 (Week 2)
#### Task 1
To get the stats:
```
 python gate.py -f ../data/auto93.csv -t stats
```

##### Output Directory: [hw/w2](hw/w2)

### HW3 (Week 3)
#### Task 1
To print the little ascii table:
```
python gate.py -f ../data/diabetes.csv -t ascii_table
python gate.py -f ../data/soybean.csv -t ascii_table
```
#### Task 3
To execute bayes on `diabetes.csv`:
```
python gate.py -t bayes
```
#### Task 4
To explore low frequency settings on `soybean.csv`:
```
python gate.py -t km
```
- Recommended low frequency settings for `soybean.csv` are `k=2` and `m=1`, as they return the best accuracy of 85%.
- Accuracy of 73% is obtained on `diabetes.csv` for low frequency settings `k ∈ {0,1,2,3}` and `m ∈ {0,1,2,3}`

##### Output Directory: [hw/w3](hw/w3)

### HW4 (Week 4)
To execute the SMO using gate function 20 times:
```
python gate.py -t gate20
```
The output files are stored in `hw/w4` directory

##### Output Directory: [hw/w4](hw/w4)

#### Question 1
Does SMO do better than the random baselines?

Answer: 

First, look to [Our Data Output](hw/w4/gate20.out). Here it can be seen that SMO does better than our random baselines nearly 100% of the time. Look at any section of the data and see for yourself. Let's take a random section in the middle, for example, let's say the 3rd run of gate. Starting [here](https://github.com/ase-spring24-team/hw1/blob/486b3803628fcd86753fdf7f23e3ac5a1fcb8804/hw/w4/gate20.out#L445) you can see that the top example in print 1 and 2 has a terrible weight, acceleration, and mpg, 3761, 9.5 and 20 respectively when compared to [print 6 row](https://github.com/ase-spring24-team/hw1/blob/486b3803628fcd86753fdf7f23e3ac5a1fcb8804/hw/w4/gate20.out#L665) (SMO) where our weight calculated was 2130, acceleration was 24.6, and mpg was 40. Even compared to [print 4](https://github.com/ase-spring24-team/hw1/blob/486b3803628fcd86753fdf7f23e3ac5a1fcb8804/hw/w4/gate20.out#L659) the ROW calculated by SMO produced a better weight, acceleration, and mpg.

#### Question 2
How many y row evaluations are required for finding the absolute best?

Answer: 

The number of evaluations required finding the absolute best is `O(#yColumns × #Data)`. For the the `auto93.csv` file, `#yColumns = 3` and `#Data = 398`. So the number of evaluation is `1194`.

#### Question 3
How does SMO do compared to absolute best?

Answer:

Our sample data shows that SMO does quite well. It often produces optimal rows nearly equal to the absolute best row calculated by evaluating all y values. For example, look at [this](https://github.com/ase-spring24-team/hw1/blob/486b3803628fcd86753fdf7f23e3ac5a1fcb8804/hw/w4/gate20.out#L887) row calculated by SMO. When compared to the [perfect row](https://github.com/ase-spring24-team/hw1/blob/486b3803628fcd86753fdf7f23e3ac5a1fcb8804/hw/w4/gate20.out#L727) it's actually quite close. Even despite not being quite as perfect as the absolute best row, SMO can calculate these optimal rows in a fraction of the time. This is especially apparent when you consider that in the real world, evaluating each y-value may take a significant amount of time, and using SMO reduces the number of y-value evaluations significantly.

### HW5 (Week 5)
#### Task 1
To run the 'Distance' function:
```
python mylo.py -t dist
```
#### Task 2
To run the 'Far' using fastmap heuristic:
```
python mylo.py -t far  
```
##### Output Directory: [hw/w5](hw/w5)

### HW6 (Week 7)
#### Task 1
To run the Recursive random projections to generate Clusters:
```
python mylo.py -t tree 
```
#### Task 2
To run the Single descent:
```
python mylo.py -t branch 
```
#### Task 3
To run Double Tap:
```
python mylo.py -t double_tap  
```
##### Output Directory: [hw/w7-hw6](hw/w7-hw6)

### HW7 (Week 8)
#### Part 1
To run the smo experiment (no stats):
```
python gate.py -t smo_exp
```
#### Part 2
To run the smo experiment (ranking stats):
```
python gate.py -t smo_ranking_stats
```
##### Output Directory: [hw/w8-hw7](hw/w8-hw7)

### HW8 (Week 9)
To run the Discretization:
```
python .\mylo.py -t bins
```
##### Output Directory: [hw/w9-hw8](hw/w9-hw8)

### HW9 (Week 10)
To run the Rules:
```
python .\mylo.py -t rules
```
##### Output Directory: [hw/w10-hw9](hw/w10-hw9)

## Team members:

- Sai Raj Thirumalai (sthirum4)
- Sam Kwiatkowski-Martin (slkwiatk)
- Sathiya Narayanan Venkatesan (svenka32)
