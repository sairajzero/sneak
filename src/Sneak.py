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
    -z --zero   close to zero                   = 0
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

def FIND(node, best_node = None, best_node_score = None, boolean = False): # dfd vector from global 
    """
    create a global node pointing to root (outside of find)
    1. check if both left and right
    2. calc scrore (3.6 and 3.7 eq)
    if the score(node) =0 (how close to 0), boolean= false else true
    3. if score is better (bigger) then global node scroe or global node score is not set yet:
        the global node is now current node
    4. recursive left and right 
    5. check boolean from left and right
    return 'or' of all 3 boolean
    ##result in global node
    Δ[vi] =xor btw left and right (cols)
    hyperparameter: how close to 0 is 0
    """
    if node.left and node.right:
        score = calc_score(node)
        if score > the.zero: # This takes care of return 'or' of all 3 boolean
            boolean = True
        if best_node_score is None or score > best_node_score:
            best_node = node
            best_node_score = score
        boolean, best_node, best_node_score = FIND(node.lefts, best_node, best_node_score)        
        boolean, best_node, best_node_score = FIND(node.rights, best_node, best_node_score)
        return boolean, best_node, best_node_score

def calc_score(node):
    global entropy, dfd
    nom = 0
    denom = 0
    delta = delta_v(node)
    for i in range(len(node.here.cols.all)):
        good_vi = entropy[i] * (1-dfd[i])
        print(good_vi)
        nom += delta[i] * good_vi
        denom += delta[i]
    
    return nom / denom

def calc_dfd(root):
    """
    dfd vector = [0] * number of columns
    if root.left:
        recursive_dfd(root.left, dfd_vector, 1)
    if root.right:
        recursive_dfd(root.right, dfd_vector, 1)
    #dfd_vector should be global

    normalize dfd_vector between 0 and 1
    """
    global dfd
    dfd = [0] * len(root.here.cols.all)
    max_depth = max(recursive_dfd(root.lefts, dfd, 1), recursive_dfd(root.rights, dfd, 1))
    dfd = normalize(dfd, max_depth)
    print(dfd, max_depth)
    return dfd

def recursive_dfd(node, dfd, depth):
    """
    1. check if both left and right
    2. for every col check if left is diff than right
    3. for the cols that are diff and dfd_vector[col] > depth || ==0, set the dfd_vector[col] = depth 
    4. recursive left and recursive right with depth=depth+1
    return nothing
    """
    if node.left and node.left:
        left = node.left.cells
        right = node.right.cells
        for i in range(len(left)):
            if left[i] != "?" and right[i] != "?":
                if left[i] != right[i] and (depth < dfd[i] or dfd[i] == 0):
                    dfd[i] = depth
        return max(recursive_dfd(node.lefts, dfd, depth+1), recursive_dfd(node.rights, dfd, depth+1)) # returns the max depth
    else:
        return depth
        

def normalize(dfd, max_depth):
    return [d/max_depth for d in dfd]

def BETTER(node, evalFn):
    left_score = evalFn(node.left)
    right_score = evalFn(node.right)
    return left_score > right_score

def SNEAK(evalFn = None):
    d = Data("../data/auto93.csv")
    tree, eval = d.tree(True)
    print(tree)
    """
    1. get the entropies 
    2. get the depth of 1st diff (dfd)
    """
    global entropy
    entropy = calc_entropy(tree)
    dfd = calc_dfd(tree)
    
    while True:
        subtree = FIND(tree) # parameters: entropy and dfd
        if not subtree:
            break
        if BETTER(subtree, evalFn):
            subtree.right = None # TODO go on the root and remove all of the rows from the root that are in the subtree of wrost
            # subtree.asked = 1 
        else:
            subtree.left = None
        entropy = calc_entropy(tree)
    """
        2. recalculate the entropy based on root (clone the data with new rows) and the new entropy values should be passsed to FIND
    """ 
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
            node.current = above
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
    SNEAK()