class DisjointSet:
    def __init__(self):
        self.parent = {}  # Dictionary to store the parent of each element
        self.s1 = -1
        self.s2= -1
        self.merging_scour = 0

    def make_set(self, element):
        # Create a new set with a single element
        self.parent[element] = element

    def find(self, element):
        # Find the representative element (root) of the set
        if self.parent[element] == element:
            return element
        return self.find(self.parent[element])

    def union(self, element1, element2):
        # Merge two sets by making one the parent of the other
        root1 = self.find(element1)
        root2 = self.find(element2)
        if root1 != root2:
            self.parent[root2] = root1
            return True
        return False
    def get_set(self, node):
        #for a given node, return the set that contains this node
        root = self.find(node)
        nodes_list=[]
        for element in self.parent:
            if root == self.find(element):
                nodes_list.append(element)
        return nodes_list

    def get_sets(self):
        sets = {}  # Dictionary to store sets and their representatives
        for element in self.parent:
            root = self.find(element)
            if root not in sets:
                sets[root] = [element]
            else:
                sets[root].append(element)
        return sets

    def is_representative(self, node):
        representative = self.find(node)
        if node == representative:
            return True
        else:
            return False

    def print(self):
        all_sets = self.get_sets()
        for representative, elements in all_sets.items():
            print(f"Set with representative {representative}: {elements}")
