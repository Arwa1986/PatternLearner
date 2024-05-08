# from matrix_reader import *

class Graph_comparision():
    def __init__(self):
        self.pairs_toCheck = []

    def are_graphs_equal(self,fsm1, fsm2):
        # Check if the number of nodes is the same
        if len(set(fsm1.apta.G.nodes)) != len(set(fsm2.apta.G.nodes)):
            return False

        # get the edge sets of both graphs
        edges1 = fsm1.apta.G.edges
        edges2 = fsm2.apta.G.edges

        # Check if the number of edges is the same
        if len(edges1) != len(edges2):
            return False

        s1 = fsm1.apta.root
        s2 = fsm2.apta.root
        self.pairs_toCheck.append([s1, s2])
        # list to keep track of all visited nodes of the first graph
        fsm1_visited = []

        while not self.all_states_are_visited(fsm1_visited, fsm1.apta.G.nodes):
            pair = self.pairs_toCheck.pop()
            s1 = pair[0]
            s2 = pair[1]
            # state0_outEdges = {'a'=state1, 'b'=state5} --> state 0 has two outgoing transitions: a to state 1 and b to state 5
            s1_outEdges = fsm1.apta.get_out_edges_asDictionary(s1)
            s2_outEdges = fsm2.apta.get_out_edges_asDictionary(s2)
            # check the Acceptance condition of the pair
            if fsm1.apta.G.nodes[s1]['type'] != fsm2.apta.G.nodes[s2]['type']:
                return False
            # Check if the number of edges and labels (of the current state) are the same
            if s2_outEdges.keys() != s2_outEdges.keys():
                return False
            else:
                for key in s1_outEdges:
                    # if the state in the first graph has a selfloop
                    # but the second hasn't for the same label
                    # then exit with false
                    if s1_outEdges[key] == s1:
                        if s2_outEdges[key] != s2:
                            return False
                    else:
                        # if there is more than one label going toward the same target_state
                        s1_sameTargetState = self.find_keys_by_value(s1_outEdges, key)
                        if s1_sameTargetState:
                            s2_targetState = s2_outEdges[key]
                            for k in s1_sameTargetState:
                                if s2_outEdges[k] != s2_targetState:
                                    return False
                        else:
                            # the target state for s1 with label=key is a state that is not the same state as s1
                            if s2_outEdges[key]==s2:
                                return False
                fsm1_visited.append(s1)
                self.update_pairs_toCheck(fsm1_visited, s1_outEdges, s2_outEdges)

                # if self.pairs_toCheck:


        return True

    def update_pairs_toCheck(self, fsm1_visited, s1_outEdges, s2_outEdges):
        for key in s1_outEdges:
            if s1_outEdges[key] not in fsm1_visited:
                s1 = s1_outEdges[key]
                s2 = s2_outEdges[key]
                if [s1,s2] not in self.pairs_toCheck:
                    self.pairs_toCheck.append([s1, s2])
        # return pair_toCheck

    def all_states_are_visited(self, fsm1_visited, fsm1_nodes):
        return len(fsm1_nodes) == len(fsm1_visited)

    def find_keys_by_value(self, input_dict, input_key):
        """
        Find keys in a dictionary that have the same value as the given key.

        Parameters:
        - input_dict (dict): The input dictionary.
        - input_key (hashable): The key to compare values against.

        Returns:
        - List: A list of keys with the same value as the given key.
        """
        # TO DO: try disjoint sets
        return [key for key, value in input_dict.items() if value == input_dict[input_key] and key!= input_key]



if __name__ == "__main__":
    pass
    # G1 = read_matrix('matrix1.adjlist')
    # draw(G1, "matrix1.png")
    # apta1 = APTA()
    # apta1.G = G1
    # fsm1 = FSM(apta1)
    #
    # G2 = read_matrix('matrix2.adjlist')
    # draw(G2, "matrix2.png")
    # apta2 = APTA()
    # apta2.G = G2
    # fsm2 = FSM(apta2)
    # GC = Graph_comparision()
    # print(f'Are Graphs equals?{GC.are_graphs_equal(fsm1, fsm2)}')

    # --- get out edges as Dictionary ---
    # test case 1
    # nodes = fsm1.apta.G.nodes
    # for s in nodes:
    #     print(f'{s}={fsm1.apta.get_out_edges_asDictionary(s)}')


    # test case 1
    # output should be True
    # dict1 = {'a':'S0', 'b':'S4'}
    # dict2 = {'b':'S3', 'a':'S5'}
    #
    # if dict1.keys() == dict2.keys():
    #     print('True')
    # else:
    #     print('False')

    # test case 2
    # output should be False
    # dict1 = {'a': 'S0', 'b': 'S4'}
    # dict2 = {'b': 'S3', 'a': 'S5', 'c':'S0'}
    #
    # if dict1.keys() == dict2.keys():
    #     print('True')
    # else:
    #     print('False')

    # Example usage
    # GC = Graph_comparision()
    # my_dict = {
    #     'a': 1,
    #     'b': 2,
    #     'c': 1,
    #     'd': 3,
    # }

    # result = GC.find_keys_by_value(my_dict, 'a')
    # print(f"Keys with the same value as 'a': {result}")

    # my_dict2 = {
    #     'a': 30,
    #     'b': 70,
    #     'c': 30,
    #     'd': 40,
    # }
    # s1_sameTargetState = find_keys_by_value(my_dict, 'a')
    # s2_targetState = my_dict2['a']
    # for k in s1_sameTargetState:
    #     if my_dict2[k] != s2_targetState:
    #         print( "False");
    # visited = [0]
    # toCheck = [[0, "00"]]
    # GC.pairs_toCheck = toCheck

    # print(GC.update_pairs_toCheck(visited, my_dict, my_dict2))

    # print("Done")