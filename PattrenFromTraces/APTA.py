from typing import List
import networkx as nx
# import matplotlib.pyplot as plt
# from IPython.display import Image
# from path import PATH

class APTA:
    figure_num = 1
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.id = 0
        self.frm = 0

        # add initial state to the graph G
        self.add_state()

        # self.max_loop_iterators = []
        # self.distance_from_root_to_all_nodes = None
        self.root = 0
        self.alphabet = []

    def add_edge(self, frm, to, lbl):
        # discover the alphabet
        if lbl not in self.alphabet:
            self.alphabet.append(lbl)
        # add edge
        self.G.add_edge(frm, to, label=lbl,  weight='1')

    def get_edge_label(self, edge_tuple):
        frm, to, key = edge_tuple[0], edge_tuple[1], edge_tuple[2]
        lbl = self.G.get_edge_data(frm, to, key)["label"]
        return lbl

    def get_out_edges(self, s):
        if s in self.G:
            return self.G.out_edges(s, keys=True)
        else:
            return []

    def get_in_edges(self, s):
        if s in self.G:
            return self.G.in_edges(s, keys=True)
        else:
            return []

    def delete_edge(self,edge_tuple):
        frm, to, key = edge_tuple[0], edge_tuple[1], edge_tuple[2]
        if edge_tuple in self.G:
            self.G.remove_edge(frm, to, key)

    # Function to get all transitions between two nodes
    def get_transitions_between_states(self, source, target):
        transitions = []
        for u, v, edge_data in self.G.edges(data=True):
            if u == source and v == target:
                transitions.append(edge_data.get('label'))
        return transitions

    def add_trace(self, trace, type):
        self.frm = 0
        # if the graph is empty add the first trace
        if self.G.number_of_nodes() == 1:
            for i in range(len(trace)):
                if i == len(trace) - 1:
                    to = self.add_state(type)
                else:
                    #  add transaction
                    to = self.add_state()
                self.add_edge(self.frm, to, trace[i])
                # the distination now become the source for the next transaction
                self.frm = to
        else:
            # for label in trace:
            x = 0
            i = 0

            for node in trace:
                if x == -1:
                    break;
                self.frm = x
                x = self.get_successor(x, trace[i])
                if i==len(trace)-1:
                    self.set_state_type(x,type)
                lable_count =i
                i = i + 1
            # if traces have duoblecate walks
            if i == len(trace) and x!= -1:
                return

            for j in range(lable_count, len(trace)):
                if j == len(trace) - 1:
                    to = self.add_state(type)
                else:
                    #  add transition
                    to = self.add_state()
                self.add_edge(self.frm, to, trace[j])
                # the distination now become the source for the next transition
                self.frm = to

    def get_successor(self, n, label):
        if len(self.G.out_edges(n, keys=True)) != 0:
            for edge in self.G.out_edges(n, keys=True):
                # print(edge)
                if self.get_edge_label(edge) == label:
                    return edge[1]
            return -1
        else:
            return -1

    def add_state(self, type="accepted"):
        # create a new state with new id and add it to the graph
        if type == "accepted":
            self.G.add_node(self.id, label=self.id, type=type, style='filled', fillcolor='gray', shape='doublecircle')
        elif type == "rejected":
            self.G.add_node(self.id, label=self.id, type=type, style='filled', fillcolor='gray', shape='square')

        # increase id for the next state
        self.id = self.id + 1
        return self.id - 1

    def get_state_type(self, s):
        if s in self.G:
            return self.G.nodes[s]["type"]
        else:
            return ""

    def change_state_label(self, source, target):
        self.G.nodes[target]["label"] = str(source) + ',' + str(target)

    def set_state_type(self, s, typ):
        if s in self.G:
            self.G.nodes[s]["type"] = typ
            if typ == "accepted":
                self.G.nodes[s]["shape"] ='doublecircle'

            elif typ == "rejected":
                self.G.nodes[s]["shape"] = 'square'

    def the_winner_type(self, s_type, t_type):
        if s_type == "unlabeled":
            return t_type
        else:
            return s_type

    def delete_state(self, s):
        if s in self.G:
            self.G.remove_node(s)

    def build_APTA(self, positive_traces, negative_traces):#, constrains):
        # self.max_loop_iterators = constrains
        for t in positive_traces:
            self.add_trace(t, "accepted")

        for t in negative_traces:
            self.add_trace(t, "rejected")
        return self.G

    def run_floyd_warshall(self):
        fw = nx.floyd_warshall(self.G, weight='eval(weight)')
        self.distance_from_root_to_all_nodes = {frm: dict(b) for frm, b in fw.items() if frm == self.root}

    def get_distance_to(self, s):
        # root = self.get_root()
        if s in self.G:
            d = self.distance_from_root_to_all_nodes[self.root][s]
        return d

    # def get_nearset(self, p1:PATH, p2:PATH):
    #     first_of_p1 = p1.get_first_state()
    #     first_of_p2 = p2.get_first_state()
    #     distance_to_p1 = self.get_distance_to(first_of_p1)
    #     distance_to_p2 = self.get_distance_to(first_of_p2)
    #
    #     if distance_to_p1 <= distance_to_p2:
    #         return p1
    #     else:
    #         return p2

    # def set_distance_to_all_paths(self, list_of_paths:List[PATH]):
    #     for p in list_of_paths:
    #         p.distance_to_root = self.get_distance_to(p.get_first_state())

    def get_self_loop(self):
        # find and list all the self-loop edges in a graph (self.G)
        # while also retrieving edge data with the key "label".
        return list(nx.selfloop_edges(self.G, data="label", keys=True))

    def has_successor(self, s):
        if s in self.G:
            successors = list(self.G.successors(s))
            if successors:
                return True
            else:
                return False

    def has_out_edge(self, state, edge):
        if state in self.G:
            out_edges = self.get_out_edges(state)
            for e in out_edges:
                if self.get_edge_label(e) == self.get_edge_label(edge):
                    return True
            return False

    def has_in_edge(self, state, edge):
        if state in self.G:
            in_edges = self.get_in_edges(state)
            for e in in_edges:
                if self.get_edge_label(e) == self.get_edge_label(edge) and e[0] == edge[0]: # the incoming edge is from the same state
                # if e == edge:
                    return True
            return False

    # Function to retrieve all children of a state
    def get_children(self, state):
        return list(self.G.successors(state))

    def get_child_nodes_with_label(self, node, label):
        edges = self.get_out_edges(node)  # edge(frm, to, key)
        for e in edges:
            if self.get_edge_label(e) == label:
                parent, child = e[0], e[1]
                return child

    def get_color(self, state):
        return self.G.nodes[state]['fillcolor']

    def set_color(self, state, color):
        self.G.nodes[state]['fillcolor'] = color

    def is_red(self, state):
        return self.G.nodes[state]['fillcolor'] == 'red'

    def is_blue(self, state):
        return self.G.nodes[state]['fillcolor'] == 'blue'

    def is_gray(self, state):
        return self.G.nodes[state]['fillcolor'] == 'gray'

    def is_all_states_red(self):
        for state in self.G.nodes:
            if not self.is_red(state):
                return False

        return True

    # red with any color = red
    # if no red and one of the states are blue = blue
    # when they all are gray = gray
    def the_winner_color(self, s1, s2):
        color = 'gray'
        if self.is_gray(s1):
            color = self.get_color(s2)
        elif self.is_red(s1) or self.is_red(s2):
            color = 'red'
        elif self.is_blue(s1) and self.is_blue(s2):
            color = 'blue'

        return color

    def reset_states_colors(self):
        for n in self.G.nodes:
            self.G.nodes[n]['fillcolor'] = 'gray'

    # is_leaf: Boolean
    # True: is the state has no children (no outgoing transition)
    # False: otherwise
    def is_leaf(self, state):
        return self.G.out_degree(state) == 0

    def delete_rejected_leaf_nodes(self):
        leaf_nodes = [node for node in self.G.nodes() if self.is_leaf(node) and self.get_state_type(node) == 'rejected']
        # print(f'leaves: {leaf_nodes}')
        self.G.remove_nodes_from(leaf_nodes)

    def draw_multiDigraph(self):
        # p = nx.drawing.nx_pydot.to_pydot(fsm.AG.G)
        p = nx.nx_agraph.pygraphviz_layout(self.G, prog='dot')
        p = nx.drawing.nx_pydot.to_pydot(self.G)
        p.write_png(f'output/figure{APTA.figure_num:02d}.png')
        APTA.figure_num+=1