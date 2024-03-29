"""

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

from the import THE, the, SLOTS
from Data import Data
from Sample import SAMPLE
from Num import Num
from Sym import Sym
from Node import Node
from Binary import Binary
import util as l
from Range import _ranges1
import sys, random

def FIND(node, depth = 1):
    out = []
    if node.left and node.right:
        good = l.entropy(node)
        out.push(good)
        

def bfs_tmp(tree, target):
        queue = []
        if tree != None:
            queue = [[tree]]
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if target == node.score:
                    return path_id, node
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return None, None

def BETTER(node, evalFn):
    left_score = evalFn(node.left)
    right_score = evalFn(node.right)
    return left_score > right_score

def SNEAK(evalFn):
    d = Data("../data/auto93.csv")
    tree = d.tree(True)
    print(tree)
    while True:
        subtree = FIND(tree)
        if not subtree:
            break
        if BETTER(subtree, evalFn):
            subtree.right = None
        else:
            subtree.left = None
    return tree

def sway(data_item, enough):
        """
        Recursive random projects. 'Half' then data, then recurse on each half.
        :param sortp: Boolean, true if sorted? I think...
        """
        def _tree(data,above = None):
            """
            Recursive tree function
            :param data:
            :param above:
            """
            node = Node(data)
            if len(data.rows) < enough:
                return node
            else:
                lefts, rights, node.left, node.right = data_item.half(data.rows,True, above)[:4]
                node.lefts = _tree(data_item.clone(lefts), node.left)
                node.rights = _tree(data_item.clone(rights), node.right)
            return node
        return _tree(data_item)

def binary():
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
    t = []
    print("OUTPUT1:")
    for col in d.cols.x:
        # iterate through the indpendent variable names
        print("")
        for range in _ranges1(col, rowss):
            # iterate through all the possible ranges
            print(l.o(range))
            t.append(range) # this might be wrong... double check this later
    
    binary_data = Binary(t, d.cols.all)
    for row in d.rows:
        binary_data.add(row.cells)
    for row in binary_data.data:
        print(row)


def run_sway():
    print(the.file)
    d = Data(the.file)
    t = sway(d, 100)
    t.show()



if __name__ == '__main__':
    #all()
    #test_sample()
    #the._set(SLOTS({"file":"../data/auto93.csv", "__help": "", "m":2, "k":1, "p":2, "Half":256, "Far":.95, "seed":31210, "Beam":10, "bins":16}))
    doc = l.settings(__doc__)
    doc = l.cli(doc)
    the._set(doc)
    random.seed(the.seed)  # set the random seed so that tests are repeatable...
    run_sway()