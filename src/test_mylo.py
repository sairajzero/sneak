"""
File created by Sathiya Narayanan Venkatesan
Examples class -- essentially just the testing mylo related functions 
"""
from the import THE, the, SLOTS
from Data import Data
from Sample import SAMPLE
from Range import Range
from Rule import Rule
from Rules import Rules
from Num import Num
from Sym import Sym
from Node import Node
import util as l
from Range import _ranges, _ranges1
import sys, random

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

def help():
    print(the.__help)
    return True

def far():
    d  = Data("../data/auto93.csv")
    far = d.farapart(d.rows)
    print("far1: ", l.o(far[0]))
    print("far2: ", l.o(far[1]))
    print("distance = ", far[2])
    return l.rnd(far[2]) == 85

def egs():
    """
    Prints out all the different tests we can run
    """
    #test_names = ["all", "egs", "help", "sym", "num", "csv", "data", "stats", "oo"]
    test_names = tests.keys()
    for test_name in test_names:
        print("python mylo.py -t " + test_name)
    return True 

def test_row_neighbors0():
    d = Data("../data/auto93.csv")
    r1 = d.rows[0]
    r2 = r1.neighbors(d)[0]
    print(l.o(r1), "==", l.o(r2))
    return r1==r2

def test_row_neighbors1():
    d = Data("../data/auto93.csv")
    r1 = d.rows[0]
    r2 = r1.neighbors(d)[1]
    print(l.o(r1), "closest", l.o(r2))
    return r1 != r2

def test_row_dist():
    d = Data("../data/auto93.csv")
    r1 = d.rows[0]
    r2 = r1.neighbors(d)[1]
    distance  = r2.dist(r1, d)
    print(l.o(r1), l.o(r2), l.rnd(distance))
    return distance == 0

def dist():
    """
    Prints the first row, sorts all the rows based on their distance to the first row,
    and then prints every 30th row with the distance of each to the first row
    """
    d = Data("../data/auto93.csv")
    r1 = d.rows[0]  # pull out the first row
    rows = r1.neighbors(d)
    for i in range(len(rows)):
        if i%30 == 0:
            print(i+1, rows[i].cells, round(rows[i].dist(r1, d),2))

def test_sym_dist_both_unknown():
    """
    Tests that the sym.dist function is working as expected when 2 "?" values are input
    """
    n = Sym()
    print(n.dist("?","?") == 1)
    return n.dist("?","?") == 1


def test_sym_dist_one_unknown():
    """
    Tests that sym.dist works as expected when only one value is unknown
    """
    n = Sym()
    print(n.dist("A","?") == 1)
    return n.dist("A","?") == 1

def test_sym_dist_both_known_and_equal():
    """
    Tests that sym dist works when both x and y are known and are equal
    """
    n = Sym()
    print(n.dist("A","A") == 0)
    return n.dist("A","A") == 0

def test_sym_dist_both_known_and_not_equal():
    """
    Tests that sym dist works when both x and y are known and are not equal
    """
    n = Sym()
    print(n.dist("A","B") == 1)
    return n.dist("A","B") == 1

def test_num_dist_both_unknown():
    """
    Tests that the num.dist function is working as expected when 2 "?" values are input
    """
    n = Num()
    assert n.dist("?","?") == 1

def test_num_dist_one_unknown():
    """
    Tests that num.dist works as expected when only one value is unknown
    """
    n = Num()
    for i in range(1, 11):
        n.add(i)  # adding nums from 1 to 10
    assert n.dist("?", 5) == 1-(4/9+1E-30)  # should be the exact output in this case
    assert n.dist(5, "?") == 1-(4/9+1E-30)  #
    assert n.dist("?", 8) == 7/9+1E-30
    assert n.dist(8, "?") == 7/9+1E-30

def test_num_dist_both_known():
    """
    Tests that num dist works when both x and y are known
    """
    n = Num()
    for i in range(1, 11):
        n.add(i)  # adding nums from 1 to 10
    assert n.dist(6, 5) == (5 / 9 + 1E-30) - (4 / 9 + 1E-30)  # should be the exact output
    assert n.dist(5, 6) == abs((4 / 9 + 1E-30)-(5 / 9 + 1E-30))

def half():
    d = Data("../data/auto93.csv")
    lefts, rights, left, right, C, cut, evals = d.half(d.rows)
    print(len(lefts), len(rights), l.rnd_list(left.cells), l.rnd_list(right.cells), l.rnd(C), l.rnd(cut), evals)

def tree():
    t, evals = Data("../data/auto93.csv").tree(True)
    t.show()
    print("evals:", evals)

def branch():
    d = Data("../data/auto93.csv")
    best, rest, evals = d.branch()
    print(l.rnd_list(best.mid().cells), l.rnd_list(rest.mid().cells))
    print("evals:", evals)

def double_tap():
    d = Data("../data/auto93.csv")
    best1, rest, evals1 = d.branch(32)
    best2, _,    evals2 = best1.branch(4)
    print(l.rnd_list(best2.mid().cells), l.rnd_list(rest.mid().cells))
    print(evals1+evals2)

def test_data_clone():
    d = Data("../data/auto93.csv")
    d_clone = d.clone(d.rows)
    print("Comparing Column", d.cols.names, "==" ,d_clone.cols.names, ":", d.cols.names == d_clone.cols.names)
    if d.cols.names != d_clone.cols.names:
        print("Data not cloned correctly: Columns differ")
        return False
    if len(d.rows) != len(d_clone.rows):
        print("Data not cloned correctly: Row length different")
    for i in range(len(d.rows)):
        if d.rows[i] != d_clone.rows[i]:
            print("Data not cloned correctly: Row", i, "not same")
            return False
    print("Comparing Rows: All rows are cloned correctly")
    return True

def test_evals():
    d = Data("../data/auto93.csv")
    _, _, evals = d.branch()
    return evals > 0

def test_node_init():
    """
    Tests that all of the attributes of the node class are initialized correctly
    """
    d = Data("../data/auto93.csv")
    node = Node(d)
    assert node.here == d
    assert node.left is None
    assert node.right is None
    assert node.C is None
    assert node.cut is None
    assert node.lefts is None
    assert node.rights is None

def test_sample():
    """
    Tests that all of the attributes of the sample class are calculated correctly
    """
    sample = SAMPLE([0.34, 0.49 ,0.51, 0.6])
    assert type(sample.has) == type([])
    assert sample.ready == False
    assert sample.txt == ""
    assert sample.rank == 0
    assert sample.n == 4
    assert round(sample.sd, 2) == 0.11
    assert round(sample.m2, 2) == 0.03
    assert round(sample.mu, 2) == 0.49
    assert round(sample.lo, 2) == 0.34
    assert round(sample.hi, 2) == 0.6

def test_num_bin():
    e = Num()
    for _ in range(1000):
        e.add(l.norm(10, 2))
    b = e.bin(10)
    return b == 9

def test_num_bin_2():
    e = Num()
    for _ in range(100):
        e.add(l.norm(10, 2))
    b = e.bin(15)
    return b == 15

def test_sym_bin():
    e = Sym()
    b = e.bin("Cloudy")
    return b == "Cloudy"

def test_range():
    """
    Tests whether all of the attributes of the range class are initialized correctly
    """
    range = Range(0, "col1", 1)
    assert range.at == 0
    assert range.txt == "col1"
    assert range.x["lo"] == 1
    assert range.x["hi"] == 1
    assert type(range.y) == type({})

def test_rule():
    """
    Tests whether all of the attributes of the rule class are working correctly
    """
    rule = Rule([Range(0, "col1", 1)])
    return "col1" in rule.parts
    print(rule.show())

def test_show():
    """
    Tests whether the show method of rule class is working correctly
    """
    rule = Rule([Range(0, "col1", 1)])
    return rule.show() == " col1 == 1 "


def bins():
    """
    This function discretizes our rows into separate bins and then prints some of them
    """
    d = Data(the.file)
    best, rest, evals = d.branch()  # included eval as not to cause an error (since branch
    #assert best.rows[0].d2h(d) < rest.rows[0].d2h(d)  # test that the best row is actually better
    # than the best row in rest
    # returns 3 values not only 2)
    LIKE = best.rows
    HATE = random.sample(rest.rows, len(rest.rows))
    rowss = {"LIKE": LIKE, "HATE": HATE}
    print("LIKE", len(LIKE), "HATE", len(HATE))
    assert len(LIKE) < len(HATE)  # test that initially like has less rows than hate
    def score(range):
        """
        Calculates the score based on the goal class for a specific range
        """
        return range.score("LIKE", len(LIKE), len(HATE)) # send goal klass, number of likes, and
        # number of hates
    t = []
    print("OUTPUT1:")
    for col in d.cols.x:
        # iterate through the indpendent variable names
        print("")
        for range in _ranges1(col, rowss):
            # iterate through all the possible ranges
            print(l.o(range))
            t.append(range) # this might be wrong... double check this later
    t = sorted(t, key=lambda range_x: score(range_x), reverse=True)  # sort the list t by each ranges score value
    max = score(t[0])  # of the newly sorted list, index 0 is now the range with the max score
    print("\n\nOUTPUT2:")
    print("\n#scores:\n")
    for range in t[0:the.Beam]:
        if score(range) > max * .1:
            print(l.rnd(score(range)), l.o(range))
    print({"LIKE": len(LIKE), "HATE": len(HATE)})  #print out the #of Likes and hates

def rules():
    d = Data(the.file)

    best0, rest, evals1 = d.branch(the.d)
    best, _, evals2 = best0.branch(the.D)
    print("Evals:", evals1 + evals2 + the.D - 1)

    LIKE = best.rows
    HATE = random.sample(rest.rows, 3 * len(LIKE))
    rowss = {"LIKE": LIKE, "HATE": HATE}

    rules = Rules(_ranges(d.cols.x, rowss), "LIKE", rowss)

    print("score\t", "mid:d2h", "row[0]:d2h\t", "mid selected\t\t\t\t\t\t", "rule")
    for rule in rules.sorted:
        result = d.clone(rule.selects(rest.rows))
        if len(result.rows) > 0:
            result.rows.sort(key=lambda x: x.d2h(d))
            print(l.rnd(rule.scored), "\t", l.rnd(result.mid().d2h(d)), "\t", l.rnd(result.rows[0].d2h(d)),"\t\t", str(l.rnd_list(result.mid().cells)).ljust(50, " "), "\t", rule.show())

def test_power_set():
    """
    Test case to ensure powerset is working correctly
    """
    li = [1,2,3]
    li_powered  = l.powerset(li)
    assert li_powered == [[], [1], [2], [2, 1], [3], [3, 1], [3, 2], [3, 2, 1]]

# function to automatically load all functions in this module in test variable
for (k, v) in list(locals().items()):
    if callable(v) and v.__module__ == __name__:
        tests[k] = v

# -- Functions below this will not be loaded as a test
def _run(t_name):
    if t_name in tests:
        return tests[t_name]()
    else:
        return None

if __name__ == '__main__':
    #all()
    #test_sample()
    the._set(SLOTS({"file":"../data/auto93.csv", "__help": "", "m":2, "k":1, "p":2, "Half":256, "d":32, "D":4,
                    "Far":.95, "seed":31210, "Beam":10, "bins":16, "Cut":.1, "Support":2}))
    random.seed(the.seed)  # set the random seed so that tests are repeatable...
    rules()
    #test_power_set()
