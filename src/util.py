"""
File created by Samuel Kwiatkowski-Martin
For util purposes such as reading in from a csv file
lines 6-18 are from professor Menzies
"""
import re
import ast
import sys
import random
import math
import fileinput
from the import SLOTS
from the import the

def coerce(val):
    try:
        return ast.literal_eval(val)
    except:
        return val.strip()


def csv(file="-"):
    with fileinput.FileInput(None if file == "-" else file) as src:
        for line in src:
            line = re.sub(r'([\n\t\r"\' ]|#.*)', "", line)
            if line:
                yield [coerce(x) for x in line.split(",")]


def settings(help_doc=__doc__):
    s = SLOTS(
        **{m[1]: coerce(m[2]) for m in re.finditer(r"--(\w+)[^=]*=\s*(\S+)", help_doc)}
    )
    s.__help = help_doc
    return s


def cli(t):
    for k, v in t.items():
        v = str(v)
        for i, s in enumerate(sys.argv):
            if s == "-" + k[0] or s == "--" + k:
                v = "False" if v == "True" else ("True" if v == "False" else sys.argv[i+1])
                t[k] = coerce(v)
    return t

def norm(mu = 0, sd = 1):
    R = random.random
    return mu + sd * math.sqrt(-2 * math.log(R())) * math.cos(2 * math.pi * R())

def rnd(n, ndecs = 2):
    if type(n) != int and type(n) != float:
        return n
    if math.floor(n) == n:
        return n
    mult = 10 ** ndecs
    return math.floor(n * mult + 0.5) / mult

def rnd_list(a, ndecs = 2):
    return list(map(lambda v: round(v, ndecs) if type(v) == float else v, a))

def oo(x): 
    print(o(x)); 
    return x

def o(x): 
    if type(x) == int or type(x) == float:
        return str(x)
    if type(x) == str:
        return x
    if type(x) == list:
        return str(x)
    elif hasattr(x, "items"):    
        return x.__class__.__name__ +"{"+ (" ".join([f"{k}:{v}" for k,v in sorted(x.items()) if k[0]!="_"]))+"}"
    else:
        return x.__class__.__name__ +"{"+ (" ".join([f"{k}:{v}" for k,v in sorted(vars(x).items()) if k[0]!="_"]))+"}"
    

def entropy(t):
    n, e = 0, 0
    for _, v in t.items():
        n += v 
    for _, v in t.items():
        e = e-v/n * math.log(v/n, 2)
    return e, n

def score(t, goal, LIKE, HATE):
    like, hate, tiny = 0, 0, 1E-30
    for klass, n in t.items():
        if klass == goal:
            like += n
        else:
            hate += n 
    like, hate = like / (LIKE + tiny), hate / (HATE + tiny)
    if hate > like :
        return 0
    else:
        return like ** the.Support / (like + hate + tiny)

def powerset(s):
    """
    This function builds a powerset of ranges s(all possible subsets of ranges)
    :param s: a list of ranges s
    """
    t = [[]]
    for x in s:
        for j in range(len(t)):
            t.append([x] + t[j])
    return t
