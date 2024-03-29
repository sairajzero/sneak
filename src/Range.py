"""
File by Sathiya Narayanan Venkatesan
This file is our Range class, distinguish sets of rows (stored in `rowss`)
"""

from collections import defaultdict
import util as l
from Sym import Sym
from the import the

class Range:
    def __init__(self, at, txt, lo, hi = None):
        """
        Initialization function for the Range class
        Sets up the column name, column index, range of x and range of y
        :param txt: column name, at: column index, lo: start of the range, hi: end of the range
        """
        self.txt = txt
        self.at = at
        self.scored =0
        self.x = { "lo": lo, "hi" : hi if hi else lo}
        self.y = {}

    def add(self, x, y):
        """
        add function for the Range class
        adds a range to the existing range
        """
        self.x["lo"] = min(self.x["lo"], x)
        self.x["hi"] = min(self.x["hi"], x)
        self.y[y] = (self.y[y] if y in self.y else 0) + 1 

    def show(self):
        """
        print function for the Range class
        prints the range based on the data
        """
        lo, hi, s = self.x["lo"], self.x["hi"], self.txt
        if lo == float("-inf"):
            return " {} < {} ".format(s, hi)
        if hi == float("inf"):
            return " {} >= {} ".format(s, lo)
        if lo == hi:
            return " {} == {} ".format(s, lo)
        return " {} <= {} < {}".format(lo, s, hi)

    def score(self, goal, LIKE, HATE):
        """
        score function for the Range class
        returns the score from the util score method
        """
        return l.score(self.y, goal, LIKE, HATE)
    
    def merge(self, other):
        """
        merge function for the Range class
        merge a range with the existing range
        """
        both = Range(self.at, self.txt, self.x["lo"])
        both.x["lo"] = min(self.x["lo"], other.x["lo"])
        both.x["hi"] = max(self.x["hi"], other.x["hi"])
        for k, v in self.y.items():
            both.y[k] = (both.y[k] if k in both.y else 0) + v 
        for k, v in other.y.items():
            both.y[k] = (both.y[k] if k in both.y else 0) + v 
        return both
    
    def merged(self, other, toofew):
        """
        merged function for the Range class
        check if the range is interesting and merge if it is
        """
        both = self.merge(other)
        e1, n1 = l.entropy(self.y)
        e2, n2 = l.entropy(other.y)
        if n1 <= toofew or n2 <= toofew:
            return both
        if l.entropy(both.y)[0] <= (n1*e1 + n2*e2) / (n1+n2):
            return both

def _ranges(cols, rowss):
    t = []
    for col in cols:
        for range in _ranges1(col, rowss):
            t.append(range)
    return t

def _ranges1(col, rowss):
    out, nrows = {}, 0
    for (y, rows) in rowss.items():
        nrows = nrows + len(rows)
        for row in rows:
            x = row.cells[col.at]
            if x != "?":
                bin = col.bin(x)
                if bin not in out:
                    out[bin] = Range(col.at, col.txt, x)
                out[bin].add(x, y)
    out = list(out.values())
    out.sort(key=lambda a: a.x["lo"])
    return out if isinstance(col, Sym) else _mergeds(out, nrows/the.bins)

def _mergeds(ranges, tooFew):
    i, t  = 0, []
    while i < len(ranges):
        a = ranges[i]
        if i < len(ranges) - 1:
            both = a.merged(ranges[i+1], tooFew)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1
    if len(t) < len(ranges):
        return _mergeds(t, tooFew)
    for i in range(1, len(t)):
        t[i].x["lo"] = t[i-1].x["hi"]
    t[0].x["lo"] = float("-inf")
    t[-1].x["hi"] = float("inf")
    return t

