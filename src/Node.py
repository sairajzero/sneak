import math 

class Node:
    def __init__(self, data):
        self.here = data
        self.current = None
        # Declare our class variables to be edited later
        self.left = None
        self.right = None
        self.C = None
        self.cut = None
        self.lefts = None
        self.rights = None

    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))  # send a boolean saying whether we are at
        # a leaf value or not --> this fun will likely be a printing statement in our context
        if self.lefts:
            self.lefts.walk(fun, depth+1)
        if self.rights:
            self.rights.walk(fun, depth+1)

    def show(self): # Print each nodes
        def d2h(data):
            return round(data.mid().d2h(self.here), 2)
        maxDepth = 0
        def _show(node, depth, leafp):
            print_cells = node.here.mid().cells
            for i in range(len(print_cells)):
                if type(print_cells[i]) == float:
                    print_cells[i] = round(print_cells[i], 2)
            post = f"{d2h(node.here)} \t{print_cells}" if leafp else f""
            nonlocal maxDepth  ## asscoiates this maxDepth with the maxDepth above the _show
            maxDepth = max(maxDepth, depth)
            print(f"{'|.. '*depth}{post}")  # print it out!
        self.walk(_show)
        # test that the max depth of recursive tree doesn't go above log2(N) where N is
        # the number of data points
        assert maxDepth <= math.log2(len(self.here.rows))
        print("")
        print_cells = self.here.mid().cells
        for i in range(len(print_cells)):
            if type(print_cells[i]) == float:
                print_cells[i] = round(print_cells[i], 2)  # round all values by 2 decimal places
        print(f"{'    '*maxDepth} {d2h(self.here)} {print_cells}")
        print(f"{'    '*maxDepth} ---- {self.here.cols.names}")

