class PATH:
    def __init__(self, sts, lbls):
        self.states= sts # list of numbers
        self.labels= lbls
        self.similar = None
        self.distance_to_root = 0 # distance between the root and the first node in the path
        self.visited = False

    def __eq__(self, other):
        return self.labels == other.labels

    def __ge__(self, other):
        return self.labels >= other.labels

    def __gt__(self, other):
        return self.labels > other.labels

    def __le__(self, other):
        return self.labels <= other.labels

    def __lt__(self, other):
        return self.labels < other.labels

    def __ne__(self, other):
        return self.labels != other.labels

    def __str__(self):
        return self.labels

    def is_mergable(self,other, G):
        last_state_of_self=  G.nodes[self.states[-1]]["type"]
        last_state_of_other =  G.nodes[other.states[-1]]["type"]
        if self == other:
            r = True
            if (last_state_of_self, last_state_of_other) == ("rejected", "accepted"):
                r = False

            if (last_state_of_self, last_state_of_other) == ("accepted", "rejected"):
                r = False
        else:
            r = False

        return r

    def has_similar(self):
        return True if self.similar else False

    def set_similar(self, similar_path):
        self.similar = similar_path

    def set_distance(self, d):
        self.distance_to_root = d

    def get_first_state(self):
        return self.states[0]

    def is_last_state(self, state):
        return state == self.states[-1]

    def get_next_state(self, state):
            index_of_next_state = self.states.index(state) + 1
            return self.states[index_of_next_state]

    def print_path(self):
        i=0
        for s in self.states:
            if i != len(self.labels):
                print(f'{s} -{self.labels[i]}-> ')
                i+=1
            else:
                print(s)
