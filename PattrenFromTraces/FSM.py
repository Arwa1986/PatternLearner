import copy
import random
from DISJOINTSETS import DisjointSet
import networkx as nx
from APTA import APTA

class FSM:
    figure_num = 2
    def __init__(self, apta:APTA):
        self.apta = apta

        red = self.apta.root
        self.apta.set_color(red, 'red')
        self.red_states = [red]

        self.good_patterns=[] # list of TemporalProperty
        self.bad_patterns=[]

    def run_EDSM_learner(self):
        if self.apta.is_all_states_red():
            return

        blue = self.pick_random_state()
        print(f'BLUE: {blue}')

        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states=[]

        valid_for_at_least_one_red = False
        for red in self.red_states:
            # print(f'RED: {red}')
            # Create a new disjoint set data structure
            ds = DisjointSet()
            ds.s1 = red
            ds.s2 = blue
            self.make_set_for_every_state_rooted_at(ds, red)
            self.make_set_for_every_state_rooted_at(ds, blue)
            self.compute_classes(ds, red, blue)


            if self.is_valid_merge(ds):
                merging_scour = self.compute_scour(ds)
                ds.merging_scour = merging_scour
                mergable_states.append(ds)
                if merging_scour > 0:
                    ds.print()
                    valid_for_at_least_one_red = True
                print(f'merging scour for {red} & {blue}: {merging_scour}')
            else:
                ds.merging_scour = -1
        if not valid_for_at_least_one_red:
             # the blue_state can't be merged with any red_state
            print(f'{blue} cannot be merged with any red_state')
            self.apta.set_color(blue, 'red') # make it red
            self.red_states.append(blue) #addit to red_states list
            self.draw()
        else:
            ds_with_highest_scour = self.pick_high_scour_pair(mergable_states)
            print(f'{ds_with_highest_scour.s1} & {ds_with_highest_scour.s2} has the highest scour : {ds_with_highest_scour.merging_scour}')
            self.merge_sets(ds_with_highest_scour)
            self.draw()
        self.update_red_states()
        self.run_EDSM_learner()

    def update_red_states(self):
        new_list = []
        for state in self.apta.G.nodes:
            if self.apta.is_red(state):
                new_list.append(state)

        self.red_states = new_list
    def make_set_for_every_state_rooted_at(self, ds, s):
        ds.make_set(s)
        descendants = nx.descendants(self.apta.G, s)
        for d in descendants:
            ds.make_set(d)

    def pick_random_state(self):
        # Get a list of all nodes (states) in the graph
        all_states = list(self.apta.G.nodes())
        # Exclude red states
        non_red_states = [s for s in all_states if self.apta.G.nodes[s].get('fillcolor') != 'red']
        # Pick a random state from the list
        random_state = random.choice(non_red_states)

        return random_state

    def compute_classes(self, ds, red, blue):
        if self.apta.is_leaf(red) or self.apta.is_leaf(blue):
            return
        have_shared_transition, shared_labels = self.have_shared_outgoing_transition(red, blue)
        if (have_shared_transition):
            ds.union(red, blue)

            for shared_label in shared_labels:
                blue_child = self.apta.get_child_nodes_with_label(blue, shared_label)
                red_child = self.apta.get_child_nodes_with_label(red, shared_label)
                ds.union(red_child,blue_child)
                self.compute_classes(ds, red_child, blue_child)
                if not ds.is_representative(red_child):
                    representative = ds.find(red_child)
                    self.compute_classes(ds, representative, blue_child)

    def is_valid_merge(self, ds):
        all_sets = ds.get_sets()
        for representative, _set in all_sets.items():
            compatible, list_type = self.is_compatible_type(_set)
            if not compatible:
                return False
        return True

    def compute_scour(self, ds):
        merging_scour = 0
        states_before_merge = self.apta.G.number_of_nodes()
        has_selfloops_before_merge = self.apta.get_self_loop()
        has_alternating_before_merge = self.getAllAlternating()

        backup = copy.deepcopy(self.apta.G)
        self.merge_sets(ds)
        states_after_merge = self.apta.G.number_of_nodes()
        self.apta.G = backup
        if states_before_merge != states_after_merge:
            merging_scour = states_before_merge - states_after_merge -1
        return merging_scour

    def merge_sets(self, ds):
        sets = ds.get_sets()
        for set in sets.items():
            represinitive, states = set
            self.merge_states(represinitive, states)

    def merge_states(self, representative, merge_list):
        list_type = self. get_list_type(merge_list)
        red = representative
        # for s in merge_list:
        #     if self.apta.get_color(s) == 'red':
        #         red = s
        target = red
        merge_list.remove(target)

        for i in range(0, len(merge_list)):
            source = merge_list[i]
            self.transfer_out_edge(source, target)
            self.transfer_in_coming_edges(source, target)

            if source == self.apta.root:
                self.apta.root = target
            if source != target:  # this if to solve butterfly problem
                self.apta.delete_state(source)
            self.apta.set_state_type(target,list_type)
        return target

    def transfer_out_edge(self, source, target):
        if source == target:
            return
        # mylist is temp list to make a copy of the out_edges list
        source_out_edges = copy.deepcopy(self.apta.get_out_edges(source))

        for e in source_out_edges:
            target_out_edges = copy.deepcopy(self.apta.get_out_edges(target))
            if self.is_in_target_out_edges(e, target_out_edges):
                continue
            temp_lbl = self.apta.get_edge_label(e)
            self.apta.delete_edge(e)
            # if the edge is a self loop in the source state move it to the target state
            if e[0] == e[1]:
                self.apta.add_edge(target, target, temp_lbl)

            else:
                self.apta.add_edge(target, e[1], temp_lbl)

        # # set type for the target state
        # s_type = self.apta.get_state_type(source)
        # t_type = self.apta.get_state_type(target)

        # self.AG.set_state_type(target, self.AG.the_winner_type(s_type, t_type))

    def is_in_target_out_edges(self, edge_tuple, edges_list):
        for e in edges_list:
            # if both edges have the same label
            if self.apta.get_edge_label(e) == self.apta.get_edge_label(edge_tuple):
                return True
        return False

    def is_self_loop(self, edge_tuple):
        return edge_tuple[0] == edge_tuple[1]

    def transfer_in_coming_edges(self, source, target):
        copylist = copy.deepcopy(self.apta.get_in_edges(source))

        for e in copylist:
            temp_lbl = self.apta.get_edge_label(e)
            if not self.apta.has_in_edge(target, e):
                self.apta.add_edge(e[0], target, temp_lbl)
            self.apta.delete_edge(e)

        # # set type for the target state
        # s_type = self.AG.get_state_type(source)
        # t_type = self.AG.get_state_type(target)
        #
        # self.AG.set_state_type(target, self.AG.the_winner_type(s_type, t_type))

    # is_compatible_type: boolean
    # return true is s1 and s2 of the same type or at least of them is unlabeled
    # return false if one is rejected the other is accepted
    def is_compatible_type(self,list):
        compatible = False
        list_type = 'unlabeled'
        if any (self.apta.get_state_type(state) == 'rejected' for state in list):
            if any(self.apta.get_state_type(state) == 'accepted' for state in list):
                # some rejected and some accepted
                compatible = False
            else: # at least one is rejected and all other are unlabeled
                compatible = True
                list_type = 'rejected'
        elif any(self.apta.get_state_type(state) == 'accepted' for state in list):
            # some are accepted and non are rejected
            list_type = 'accepted'
            compatible = True
        else:
            # all unlabeled
            compatible = True
            list_type = 'unlabeled'

        return compatible, list_type

    def get_list_type(self, merge_list):
        _c, typ = self.is_compatible_type(merge_list)
        return typ

    # have_shared_outgoing_transition: Boolean
    # True: if both states have shard a outgoing transition with the same label
    # the next state doesn't matter
    # False: if both states have totally different outgoing transitions
    def have_shared_outgoing_transition(self, state1, state2):
        share_label = False
        shared_labels =[]
        for u, v, edge_data in self.apta.G.out_edges(state1, data=True):
            label1 = edge_data.get('label')
            for _, next_state, next_edge_data in self.apta.G.out_edges(state2, data=True):
                label2 = next_edge_data.get('label')
                if label1 == label2:
                    share_label =  True
                    shared_labels.append(label1)
        return share_label, shared_labels

    def pick_high_scour_pair(self, list_of_mergable_states):# list of disjoint_sets object
        # Sort the list of lists based on the merging_scour (3rd item)
        list_of_mergable_states.sort(key=lambda x: x.merging_scour, reverse=True)

        # pick up the pair with the highest scour
        ds_with_highest_scour = list_of_mergable_states.pop(0)

        return ds_with_highest_scour
    def add_child(self, red, blue, b_child):
        transitions = self.apta.get_transitions_between_states(blue,b_child)
        for label in transitions:
            self.apta.add_edge(red, b_child, label)

    def draw(self):
        p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
        p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
        p.write_png(f'output/figure{FSM.figure_num:02d}.png')
        FSM.figure_num+=1