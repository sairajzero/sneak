"""
File by Sathiya Narayanan Venkatesan
This file is our Rule Class
"""

import util as l

class Rule:
    def __init__(self, ranges):
        """
        Initialization function for the Rule class
        :param ranges: list of ranges
        """
        self.parts = {}
        self.scored = 0

        for range in ranges:
            t = self.parts[range.txt] if range.txt in self.parts else []
            t.append(range)
            self.parts[range.txt] = t

    def _or(self, ranges, row):
        x = row.cells[ranges[0].at]
        if x == "?":
            return True
        for range in ranges:
            lo, hi = range.x["lo"], range.x["hi"]
            if lo == hi if lo == x else lo <= x and x < hi:
                return True
        return False

    def _and(self, row):
        for ranges in self.parts.values():
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows):
        t = []
        for row in rows:
            if self._and(row):
                t.append(row)
        return t

    def selectss(self, rowss):
        t = {}
        for y, rows in rowss.items():
            t[y] = len(self.selects(rows))
        return t

    def show(self):
        ands = []
        for _, ranges in self.parts.items():
            ors = _showless(ranges)
            at = 0
            for i, range in enumerate(ors):
                at = range.at
                ors[i] = range.show()
            ands.append(" or ".join(ors))
        return " and ".join(ands)

def _showless(t, ready = True):
    if not ready:
        t = t.copy()
        t = sorted(t, key=lambda a, b : a.x.lo < b.x.lo)
    i = 0
    u = []
    while i < len(t):
        a = t[i]
        if i < len(t) -1:
            if a.x["hi"] == t[i+1].x["lo"]:
                a = a.merge(t[i+1])
                i += 1
        u.append(a)
        i += 1
    return t if len(u) == len(t) else _showless(u, ready)


