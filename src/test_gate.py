"""
File created by Samuel Kwiatkowski-Martin
Examples class -- essentially just the testing class
"""
from Data import Data
from Row import Row
from Num import Num
from Sym import Sym
import Sample
from datetime import date, datetime
from util import norm, rnd
import util as l
from the import THE, the, SLOTS
import random
from statistics import mean, stdev

tests = {}


def all():
    bad = 0
    good = 0
    for t_name in tests:
        if t_name != "all":
            print("--testing:", t_name)
            if tests[t_name](): # test passed                
                good += 1
                print("Passed")
            else: # test failed
                bad += 1
                print("Failed")
    print("----")
    print("TOTAL:", bad+good)
    print("PASS:", good)
    print("FAIL:", bad)
    exit(bad)

def stats():
    """
    Tests and prints out default for the stats function on auto93.csv
    """
    stat = Data("../data/auto93.csv").stats()
    o_stat = l.o(stat)
    print(o_stat)
    return o_stat == "dict{.N:397 Acc+:15.57 Lbs-:2970.42 Mpg+:23.84}"


def num():
    e = Num()
    for _ in range(1000):
        e.add(norm(10, 2))
    mu, sd = e.mid(), e.div()
    print(rnd(mu, 3), rnd(sd, 3), mu, sd)
    return 9.9 < mu and mu < 10.5 and 2 < sd and sd < 5

def num_2():
    e = Num()
    for _ in range(500):
        e.add(norm(10))
    mu, sd = e.mid(), e.div()
    print(rnd(mu, 3), rnd(sd, 3), mu, sd)
    return 9.9 < mu and mu < 10.2 and 0.9 < sd and sd < 1.2

def sym():
    s = Sym()
    l = [1,1,1,1,2,2,3]
    for x in l:
        s.add(x)
    mode = s.mid()
    e = s.div()
    print(mode, rnd(e, 3))
    return mode == 1 and e > 1.37 and e < 1.38

def egs():
    """
    Prints out all the different tests we can run
    """
    #test_names = ["all", "egs", "help", "sym", "num", "csv", "data", "stats", "oo"]
    test_names = tests.keys()
    for test_name in test_names:
        print("python gate.py -t " + test_name)
    return True

def data():
    n = 0
    d = Data(the.file)
    for i, row in enumerate(d.rows):
        if i % 100 == 0:
            n+= len(row.cells)
            l.oo(row.cells)
    l.oo(d.cols.x[0])
    return n == 32

def csv(src = "../data/auto93.csv"):
    n = 0
    for i, t in enumerate(l.csv(src)):
        if i % 100 == 0:
            n = n + len(t)
        print(i, t)
    return n == 32

def help():
    print(the.__help)
    return True

def oo():
    d = {"a":1,"b":2,"c":3,"d":4}
    print(d)
    print(l.o(d))
    return l.o(d) == "dict{a:1 b:2 c:3 d:4}" 

def oo_2():
    d = {"a":"x","b":"y","c":"z"}
    print(d)
    print(l.o(d))
    return l.o(d) == "dict{a:x b:y c:z}" 

def row():
    """
    Tests the row class
    """
    print("[1, 2, 3] == " + str(Row([1,2,3]).cells))
    return "[1, 2, 3]" == str(Row([1,2,3]).cells)

def row_2():
    print("[5, 4, 3] == " + str(Row([5, 4, 3]).cells))
    return "[5, 4, 3]" == str(Row([5, 4, 3]).cells)

def sym_like():
    """
    Tests the like function of Sym class
    """
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/weather.csv",lambda data, t: learn(data,t,wme))
    data = wme.datas["no"]
    prior = (len(data.rows) + the.k) / (wme.n)
    like = data.cols.x[0].like("rainy", prior)
    print("like - ",like)
    return like > 0.36


def num_like():
    """
    Tests the like function of Num class
    """
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/weather.csv",lambda data, t: learn(data,t,wme))
    data = wme.datas["yes"]
    prior = (len(data.rows) + the.k) / (wme.n)
    like = data.cols.x[1].like(70, prior)
    print("like - ",like)
    return like > 0.01


def bayes():
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/diabetes.csv",lambda data, t: learn(data,t,wme))
    print("Accuracy:", wme.acc/(wme.tries))
    return wme.acc/(wme.tries) > .72

def bayes_2():
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/soybean.csv",lambda data, t: learn(data,t,wme))
    print("Accuracy:", wme.acc/(wme.tries))
    return wme.acc/(wme.tries) > .8

def bayes_3():
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/weather.csv",lambda data, t: learn(data,t,wme))
    print(wme.acc/(wme.tries))
    return wme.acc/(wme.tries) > .35

def ascii_table(file_name = None):
    if not file_name: 
        file_name = the.file
    # auto93.csv file doesnot have a klass
    if file_name == "../data/auto93.csv":
        return True
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data(file_name,lambda data, t: learn(data,t,wme))
    datas = wme.datas 
    print("Number of classes,", len(datas), ",")
    print("Total number of rows,", wme.n, ",")
    print("Class Name, number of rows, percetange")
    for key, values in datas.items():
        print(key,",", len(values.rows),",", len(values.rows) / wme.n)
    return True

def ascii_table_diabetes():
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/diabetes.csv",lambda data, t: learn(data,t,wme))
    datas = wme.datas 
    print("Class Name, number of rows, percetange")
    for key, values in datas.items():
        print(key,",", len(values.rows),",", len(values.rows) / wme.n)
    print("Total,,")
    print("Number of classes,", len(datas), ",")
    print("Total number of rows,", wme.n, ",")
    return True

def ascii_table_soybean():
    wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0}) 
    Data("../data/soybean.csv",lambda data, t: learn(data,t,wme))
    datas = wme.datas 
    print("Class Name, number of rows, percetange")
    for key, values in datas.items():
        print(key,",", len(values.rows),",", len(values.rows) / wme.n)
    print("Total,,")
    print("Number of classes,", len(datas), ",")
    print("Total number of rows,", wme.n, ",")
    return True

def global_the():
    t = THE()
    t._set(SLOTS({"a":1, "b": "xyz", "c":True}))
    print({"a":t.a, "b": t.b, "c":t.c})
    t.a = 2
    print({"a":t.a, "b": t.b, "c":t.c})
    return t.a == 2 and t.b == "xyz" and t.c == True

def km():
    """
    This function tests soybean.csv by changing around the hyperparameters k and m
    """
    best_acc = best_k = best_m = -1
    print(f"Accuracy,K,M")
    for k in range(4):
        for m in range(4):
            #  loop through all the hyperparameters
            the.k = k
            the.m = m
            wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0})
            Data("../data/soybean.csv",lambda data, t: learn(data,t,wme))
            print(f"{round(wme.acc / wme.tries, 2)},{k},{m}")
            if best_acc < (wme.acc / wme.tries):
                best_acc = (wme.acc / wme.tries)
                best_k = k
                best_m = m
    print("BEST,,")
    print(f"{round(best_acc,2)},{best_k},{best_m}")
    return best_k ==2 and best_m == 1

def km_2():
    """
    This function tests soybean.csv by changing around the hyperparameters k and m
    """
    best_acc = best_k = best_m = -1
    print(f"Accuracy,K,M")
    for k in range(4):
        for m in range(4):
            #  loop through all the hyperparameters
            the.k = k
            the.m = m
            wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0})
            Data("../data/diabetes.csv",lambda data, t: learn(data,t,wme))
            print(f"{round(wme.acc / wme.tries, 2)},{k},{m}")
            if best_acc < (wme.acc / wme.tries):
                best_acc = (wme.acc / wme.tries)
                best_k = k
                best_m = m
    print("BEST,,")
    print(f"{round(best_acc,2)},{best_k},{best_m}")
    return best_acc > 0.72

def test_heaven():
    d = Data([['Lbs-', 'Acc+']])
    print({d.cols.y[0].txt: d.cols.y[0].heaven, d.cols.y[1].txt: d.cols.y[1].heaven})
    return d.cols.y[0].heaven == 0 and d.cols.y[1].heaven == 1

def gate20():
    flag = True
    for i in range(20):
        d = Data("../data/auto93.csv")
        _stats, _bests = d.gate(4, 16, .5)
        stat, best = _stats[-1], _bests[-1]
        print("gate20", l.rnd(best.d2h(d)), l.rnd(stat.d2h(d)))
        if best.d2h(d) > stat.d2h(d):
            flag = False
    return flag

def test_20_shuffles():
    """
    Tests if the rows are being shuffled everytime between runs of gate
    """
    for i in range(20):
        d = Data("../data/auto93.csv")
        _stats, _bests = d.gate(4, 16, .5, "shuffle")
        stat, best = _stats[-1], _bests[-1]
        print(best)
        print("gate20", l.rnd(best.d2h(d)), l.rnd(stat.d2h(d)))

def test_best_less_than_rest():
    """
    Tests that best is always less then rest
    """
    budget0 = 4
    budget = 16
    some = .5
    passed = True
    for i in range(20):
        d = Data("../data/auto93.csv")
        rows = random.sample(d.rows, len(d.rows))  # shuffles rows
        lite = rows[0:budget0]  # grab first budget0 amount of rows
        for i in range(budget):
            best, rest = d.best_rest(lite, len(lite) ** some)  # sort our known rows into good vs bad
            if len(best.rows) > len(rest.rows): ## plus one for wiggle room
                passed = False

    return passed

def test_gate():
    d = Data("../data/auto93.csv")
    _stats, _bests = d.gate(4, 16, .5)
    stat, best = _stats[-1], _bests[-1]
    print(best.cells)
    print("gate", l.rnd(best.d2h(d)), l.rnd(stat.d2h(d)))
    return best.d2h(d) < stat.d2h(d)

def test_d2h():
    """
    Tests if the d2h fucntion is returning the correct values
    """
    d = Data("../data/auto93.csv")
    print(rnd(d.rows[0].d2h(d)))
    
    return rnd(d.rows[0].d2h(d)) == 0.8


def test_d2h2():
    """
    Tests if the d2h fucntion is returning the correct values
    """
    d = Data("../data/auto93.csv")
    print(rnd(d.rows[15].d2h(d)))

    return rnd(d.rows[15].d2h(d)) == 0.85

def test_d2h_sort():
    """
    Tests if the sorting using d2h values is done right
    """
    d = Data("../data/auto93.csv")
    rows = random.sample(d.rows, 10)
    rows.sort(key=lambda x: x.d2h(d))
    pre = rnd(d.rows[0].d2h(d))

    for i in range(10):
        next = rnd(d.rows[i].d2h(d))
        if next < pre:
            return False
    
    print("The rows are sorted based on d2h value")
    return True

def smo_exp():
    print("Date:", datetime.now())
    print("File:", the.file)
    repeats = 20
    print("repeats:", repeats)
    print("seed:", the.seed)
    random.seed(the.seed)
    d = Data(the.file)
    print("rows:", len(d.rows))
    print("cols:", len(d.cols.names))

    # print column names
    print("names\t", d.cols.names, "\tD2h")

    # print mid and div
    mid = d.mid()
    print("mid\t", l.rnd_list(mid.cells), "\t", l.rnd(mid.d2h(d)))
    div = d.div()
    print("div\t", l.rnd_list(div.cells), "\t", l.rnd(div.d2h(d)))

    # Run smo9 20 times and print the best value in each iteration
    print("#")
    for i in range(20):
        _stats, _best = d.gate(4, 9, .5, False)
        print("smo9\t", _best[-1].cells, "\t", l.rnd(_best[-1].d2h(d)))

    # Pick 50 random and get the best (20 iterations)
    print("#")
    for i in range(20):
        rows = random.sample(d.rows, 10)
        rows.sort(key=lambda x: x.d2h(d))
        print("any50\t", rows[0].cells, "\t", l.rnd(rows[0].d2h(d)))

    # Evaluate all data to find the best
    print("#")
    rows = d.rows.copy() # create a shallow copy of the array (to sort)
    rows.sort(key=lambda x: x.d2h(d))
    print("100%\t", rows[0].cells, "\t", l.rnd(rows[0].d2h(d)))
    

def test_b_and_r():
    """
    Tests if the sorting using d2h values is done right
    """
    budget0 = 4
    some = .5
    d = Data("../data/auto93.csv")
    rows = d.rows
    lite = rows[0:budget0]  
    dark = rows[budget0:]
    best, rest = d.best_rest(lite, len(lite)**some)
    b = dark[0].like(best, len(lite), 2)
    r = dark[0].like(rest, len(lite), 2)
    print(b,r)

    if isinstance(b, (int, float, complex)) and isinstance(r, (int, float, complex)):
        print("The values of b and r are numbers")
        return True
    else:
        print("The values of b and r are not numbers")
        return False

def test_learn(learned):
    """
    Test function to make sure that learn doesn't add data before it runs likes on the row
    that is trying to be added
    """
    assert learned
    # will throw error if somehow the data gets added before being learned on
def test_likes():
    """
    Test function to make sure that the likes function is working correctly
    """
    for k in range(4):
        for m in range(4):
            #  loop through all the hyperparameters
            the.k = k
            the.m = m
            wme = SLOTS({"acc": 0, "datas": {}, "tries": 0, "n": 0})
            Data("../data/test2.csv",lambda data, t: learn(data,t,wme))
            print(wme.acc/(wme.tries))
            new_row = Row(["Sunny", "Cool", "High", "True", "?"])
            yes = new_row.like(wme.datas["yes"], 15, 2)
            no = new_row.like(wme.datas["no"], 15, 2)
            normalized_yes = yes/(yes+no)
            normalized_no = no/(yes+no)
            print(normalized_yes)
            print(normalized_no)
            print(k,m)
            print()

def smo_ranking_stats():
    """
    Runs smo bonr and rand and assembles groups of best solutions based on these runs, then
    it stratifies each group into rankings to see if each group is significantly different from
    each other or not
    """
    d = Data(the.file)  # just set d for easy use in print statements
    print_ranking_analysis(d)
    all_rows = d.rows
    # Now we must sort all rows based on the distance to heaven to get our ceiling
    all_rows.sort(key=lambda x: x.d2h(d))
    ceiling = l.rnd(all_rows[0].d2h(d))  # set ceiling value to best value
    bonr9_best_list = []  # the list of 20 best bonr9 value
    rand9_best_list = []  # the list of 20 best rand9 value
    bonr15_best_list = []
    rand15_best_list = []
    bonr20_best_list = []
    rand20_best_list = []
    rand358_best_list = []
    print("Calculating Best and Tiny...")
    for i in range(20):
        # iterate our 20 times
        bonr9_best_list.append(get_best_bonr(9))  # calls to a function that runs data for bonr9
        # and returns the best value once
        rand9_best_list.append(get_best_rand(9))  # calls to function which randomly samples
        # 9 rows from the data set and returns the best rows d2h
        bonr15_best_list.append(get_best_bonr(15))
        rand15_best_list.append(get_best_rand(15))
        bonr20_best_list.append(get_best_bonr(20))
        rand20_best_list.append(get_best_rand(20))
        rand358_best_list.append(get_best_rand(358))
    base_line_list = get_base_line_list(d.rows, d)  # returns a list of all rows d2h values
    std = stdev(base_line_list)  # standard deviation of all rows d2h values  
    print(f"Best : {ceiling}")  #  
    print(f"Tiny : {l.rnd(.35*std)}")  # WE NEED to change this later...

    print("base bonr9 rand9 bonr15 rand15 bonr20 rand20 rand358")
    print("Ranking Report: ")
    #  Below is the code that will actually stratify and print the different treatments
    Sample.eg0([
        Sample.SAMPLE(bonr9_best_list, "bonr9"),
        Sample.SAMPLE(rand9_best_list, "rand9"),
        Sample.SAMPLE(bonr15_best_list, "bonr15"),
        Sample.SAMPLE(rand15_best_list, "rand15"),
        Sample.SAMPLE(bonr20_best_list, "bonr20"),
        Sample.SAMPLE(rand20_best_list, "rand20"),
        Sample.SAMPLE(rand358_best_list, "rand358"),
        Sample.SAMPLE(base_line_list, "base"),
    ])

def test_bonr_better_than_base():
    """
    This test checks to make sure that bonr is outperforming the baseline
    """
    d = Data(the.file)  # just set d for easy use in print statements
    bonr9_best_list = []  # the list of 20 best bonr9 value
    bonr15_best_list = []
    bonr20_best_list = []
    for i in range(50):
        # iterate 50 times
        bonr9_best_list.append(get_best_bonr(9))  # calls to a function that runs data for bonr9
        # and returns the best value once
        bonr15_best_list.append(get_best_bonr(15))
        bonr20_best_list.append(get_best_bonr(20))
    base_line_list = get_base_line_list(d.rows, d)  # returns a list of all rows d2h values
    base_line_d2h = mean(base_line_list)
    # loop through all bonr9 computed values and compare to baseline value
    # it should hopefully be the case that the baseline is always worse, otherwise we might have
    # changed the code too much
    for d2h_val in bonr9_best_list:
        assert d2h_val < base_line_d2h
    for d2h_val in bonr15_best_list:
        assert d2h_val < base_line_d2h
    for d2h_val in bonr20_best_list:
        assert d2h_val < base_line_d2h

# function to automatically load all functions in this module in test variable
for (k, v) in list(locals().items()):
    if callable(v) and v.__module__ == __name__:
        tests[k] = v

# -- Functions below this will not be loaded as a test

def learn(data, row, my):
    my.n += 1
    kl = row.cells[data.cols.klass.at]
    learned = False
    if my.n > 0:
        my.tries += 1
        my.acc += (1 if kl == row.likes(my.datas)[0] else 0) # usiing [0] as we are comparing 'kl' to only 'out' in Row.likes return
        learned = True
    my.datas.setdefault(kl, Data([data.cols.names]))
    test_learn(learned)
    my.datas[kl].add(row)

def get_best_bonr(num):
    """
    Runs bonrN once and returns the best d2h value found
    """
    d = Data(the.file)
    _stats, _bests = d.gate(4, num-4, .5, False) # bonr9 if num = 9, bonr15 if num = 15 etc.
    # I also added a parameter above so that we don't have to always print all the baselines
    # when running gate
    stat, best = _stats[-1], _bests[-1]
    #print(best.d2h(d))
    #print(_bests[0].d2h(d))
    assert best.d2h(d) <= _bests[0].d2h(d)  # Tests that we are getting the best value based on d2h
    # and not some other value by accident
    return l.rnd(best.d2h(d))

def get_best_rand(num):
    """
    Runs randN once and returns the best d2h value found for the sample of num numbers
    """
    d = Data(the.file)
    rows = random.sample(d.rows, num)  # sample N number of random rows
    rows.sort(key=lambda x: x.d2h(d))  # sort the rows by d2h and pull out the best value
    return l.rnd(rows[0].d2h(d))  # return the d2h of the best row

def get_base_line_list(rows,d):
    """
    Takes a list of all rows in the data set d, and returns a list of all row's d2h values
    :param rows: list of all rows in data d
    """
    d2h_list = []
    for row in rows:
        d2h_list.append(row.d2h(d))
    return d2h_list

def print_ranking_analysis(d):
    """
    Prints out the ranking analysis
    """
    print("Starting ranking analysis...")
    # found date code at https://www.programiz.com/python-programming/datetime/current-datetime
    today = date.today()
    todays_date = today.strftime("%B %d, %Y")
    print(f"Date : {todays_date}")  # print current date
    print(f"File : {the.file}")  # print file name
    print(f"Repeats : 20")  # print the number of repetitions(num of times we run bonr15
    # when building our sampling group for example)
    print(f"Seed : {the.seed}")
    print(f"Rows : {len(d.rows)}")
    print(f"Columns : {len(d.cols.all)}")

def _run(t_name):
    if t_name in tests:
        return tests[t_name]()
    else:
        return None

if __name__ == '__main__':
    #all()
    the._set(SLOTS({"file":"../data/auto93.csv", "__help": "", "m":2, "k":1, "seed":31210}))
    random.seed(the.seed)
    #ascii_table("../data/soybean.csv")
    #km()
    #bayes()
    #test_likes()
    #gate1()
    #test_20_shuffles()
    #test_d2h_sort()
    #test_best_less_than_rest()
    #gate20()
    #test_d2h2()
    #test_bonr_better_than_base()
    smo_exp()
