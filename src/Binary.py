from Num import Num
from Sym import Sym

class Binary:
    def __init__(self, ranges, cols) -> None:
        self.__ranges = {}
        self.__order = []
        self.__cols = cols
        for range in ranges:
            if range.at not in self.__ranges:
                self.__ranges[range.at] = []
                self.__order.append(range.at)
            self.__ranges[range.at].append(range)
        self.__col_size = len(ranges)
        self.data = []
    

    def add(self, row):
        t = []
        for i in range(len(row)):
            if i in self.__order:
                t += self.bin(i, row[i])
        self.data.append(t)
    
    def bin(self, at, val):
        ranges = self.__ranges[at]
        if type(self.__cols[at]) == Num:
            for i, range in enumerate(ranges):
                if val >= range.x["lo"] and val <= range.x["hi"]:
                    bins = [0] * len(ranges)
                    bins[i] = 1
                    return bins
        elif type(self.__cols[at]) == Sym:
            for i, range in enumerate(ranges):
                if val == range.x["lo"]:
                    bins = [0] * len(ranges)
                    bins[i] = 1
                    return bins
    