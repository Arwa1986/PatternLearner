class TemporalProperty:
    def __init__(self, e1, e2, patrn):
        self.event1 = e1
        self.event2 = e2
        self.pattern = patrn
        self.counter = 0


    def print(self):
        print(f'({self.event1}, {self.event2}) - {self.pattern}: {self.counter} -> {self.get_weigth()}')

    def __eq__(self, other):
        return self.event1 == other.event1 and self.event2==other.event2 and self.pattern == other.pattern

    def get_length(self):
        #complex patterns are given higher length
        pattern_length = 0
        if self.pattern == 'Selfloop':
            pattern_length = 1
        elif self.pattern == 'Alternating':
            pattern_length = 2
        elif self.pattern == 'Eventually':
            pattern_length = 3

        return pattern_length

    def get_weigth(self):
        # weight a pattern:
        # the number of times it is satisfied
        # and multiply it by the 'length' of the pattern
        # which means that complex patterns that are satisfied would
        # be given greater weight
        return self.counter * self.get_length()