"""
File by Samuel Kwiatkowski-Martin
This is our Rules class. Notice the 's' at the end. This class manages the process of scoring ranges
, trying all their combinations, scoring the combinations and returning the result
"""
import util as l
from Rule import Rule
from the import the

class Rules:
    def __init__(self, ranges, goal, rowss):
        """
        Initialization function for the Rules class
        :param ranges: list of ranges
        :param goal: a string that is either the goal of "LIKE" or the goal of "HATE"
        :param rowss: a table that has the following key value pair structure:
        {"LIKE": [rows in best], "HATE": [3\*N of rest, selected at random]}
        """
        self.sorted = []
        self.goal = goal
        self.rowss = rowss
        self.LIKE = 0
        self.HATE = 0

        # print out all HATE and LIKE with the number in each currently
        for key, rows in rowss.items():
            print(key, len(rows))

        self.likeHate()
        assert self.LIKE == len(rowss["LIKE"])
        assert self.HATE == len(rowss["HATE"])
        for range in ranges:
            range.scored = self.score(range.y)
        self.sorted = self.top(self.trys(self.top(ranges)))

    def likeHate(self):
        """
        This function serves to determine how many rows fit our goal (LIKE), and how many
        do not (HATE)
        """
        for y, rows in self.rowss.items():
            if y == self.goal:
                # if the class is the same as our goal, then add the number of rows in that class
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        """
        Function scores our range
        :param t: a ranges y dictionary
        """
        return l.score(t, self.goal, self.LIKE, self.HATE)

    def trys(self, ranges):
        """
        Function builds all the possible rules with their scores
        :param ranges: a list of ranges
        """
        u = []
        for subset in l.powerset(ranges):
            if len(subset) > 0:
                rule = Rule(subset)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t):
        """
        Function gets the top rules with the best scores
        :param t: the list of rules to sort and pull from
        """
        t.sort(key=lambda x: x.scored, reverse=True)  # sort in decending order
        # test that are sort was correct
        assert t[0].scored > t[-1].scored
        u = []
        for x in t:
            if x.scored >= t[0].scored * the.Cut:
                # only take a certain amount of rules within the.Cut
                # aka ignore ranges that are less than C*max
                u.append(x)
        return u[:the.Beam]
