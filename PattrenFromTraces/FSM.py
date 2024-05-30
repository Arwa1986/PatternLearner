# import copy
# import random
from PattrenFromTraces.DISJOINTSETS import DisjointSet
# import networkx as nx
# from APTA import APTA
from PattrenFromTraces.Merger import *
# from PattrenFromTraces.PatternsChecker import *
from PattrenFromTraces.negative_patterns2 import *

class FSM:
    figure_num = 2
    def __init__(self, apta:APTA, all_properties, avgScour, reference_DFA):
        self.apta = apta
        self.all_properties = all_properties
        self.properties_average_scour = avgScour
        red = self.apta.root
        self.apta.set_color(red, 'red')
        self.red_states = [red]
        self.found_blue=False
        self.visited=[]
        self.blue_states=[]

        self.selfloppPat_rejectedCount=0
        self.alternatingPat_rejectedCount=0
        self.nextPat_rejectedCount=0

        self.negative_patterns = get_negative_patterns(reference_DFA)
    def run_EDSM_learner(self):
        if self.apta.is_all_states_red():
            return

        self.found_blue = False
        self.blue_states = []
        self.visited = []
        self.pick_next_blue2(self.apta.root)
        # print(f'BLUE_STATES: {self.blue_states}')
        # self.draw()
        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states=[]
        valid_for_at_least_one_red = False
        for blue in self.blue_states:
            for red in self.red_states:
                # print(f'BLUE: {blue} - RED: {red}')
                # Create a new disjoint set data structure
                ds = DisjointSet()
                ds.s1 = red
                ds.s2 = blue
                self.make_set_for_every_state_rooted_at(ds, red)
                self.make_set_for_every_state_rooted_at(ds, blue)
                work_to_do = {}
                _a = ds.union(red, blue)
                work_to_do[ds.find(red)] = ds.get_set(red)
                self.compute_classes2(ds, work_to_do)
                # have_shared_transition, shared_labels = self.have_shared_outgoing_transition(red, blue)
                # work_to_do = {}
                # if have_shared_transition:
                #     add_new_state = ds.union(red, blue)
                #     work_to_do[ds.find(red)] = ds.get_set(red)
                #     if add_new_state:
                #         self.compute_classes2(ds,work_to_do)

                if is_valid_merge(self.apta, ds):
                    # merging_scour = self.compute_scour_with_negative_patterns(ds)
                    merging_scour = self.compute_scour(ds)
                    ds.merging_scour = merging_scour
                    mergable_states.append(ds)
                    if merging_scour > 0 :
                        # ds.printSets()
                        valid_for_at_least_one_red = True
                        # print(f'Valid merge: scour for {red} & {blue}: {merging_scour}')
                    # elif merging_scour == 0:
                    #     print(f'Valid but no evidence: scour for {red} & {blue}: {merging_scour}')
                else:
                    ds.merging_scour = -1
                    # print(f'InValid merge: scour for {red} & {blue}: {ds.merging_scour}')

        # for ds_item in mergable_states:
        #     print(
        #         f'Other pairs: [{ds_item.s1}({self.apta.get_state_reference_label(ds_item.s1)}), {ds_item.s2}({self.apta.get_state_reference_label(ds_item.s2)}), {ds_item.merging_scour}]')

        if not valid_for_at_least_one_red:
            # the blue_state can't be merged with any red_state
            # print(f'{blue} cannot be merged with any red_state')
            self.apta.set_color(blue, 'red') # make it red
            self.red_states.append(blue) #addit to red_states list
            # self.draw()
        else:
            # print(f'mergable_states:')
            # for ds in mergable_states:
            #     ds.printInitialStatesAndScore()
            ds_with_highest_scour = self.pick_high_scour_pair(mergable_states)
            # self.print_pair_label(ds_with_highest_scour,mergable_states, self.apta)
            # print(f'____________________________________________________________')
            merge_sets(ds_with_highest_scour, self.apta)

            # self.draw()

        self.update_red_states()
        self.run_EDSM_learner()

    # have_shared_outgoing_transition: Boolean
    # True: if both states have shard a outgoing transition with the same label
    # the next state doesn't matter
    # False: if both states have totally different outgoing transitions
    def have_shared_outgoing_transition(self, state1, state2):
        global apta
        share_label = False
        shared_labels = []
        for u, v, edge_data in self.apta.G.out_edges(state1, data=True):
            label1 = edge_data.get('label')
            for _, next_state, next_edge_data in self.apta.G.out_edges(state2, data=True):
                label2 = next_edge_data.get('label')
                if label1 == label2:
                    share_label = True
                    shared_labels.append(label1)
        return share_label, shared_labels

    def pick_next_blue2(self, red):
            if self.found_blue:
                return
            if red in self.red_states:
                self.visited.append(red)
                # Get a list of all nodes (states) in the graph
                all_states = self.apta.get_children(red)
                # Exclude red states
                self.blue_states = [s for s in all_states if self.apta.G.nodes[s].get('fillcolor') != 'red']
                for non_red in self.blue_states:
                    self.apta.set_color(non_red, 'blue')

                if self.blue_states:
                    self.found_blue = True
                    return
                else:
                    neighbors = self.apta.get_children(red)
                    for vs in self.visited:
                        if vs in neighbors:
                            neighbors.remove(vs)
                    if red in neighbors:
                        neighbors.remove(red)
                    for neighbor in neighbors:
                        self.pick_next_blue2(neighbor)  # Recursive call to explore neighbors

    def update_red_states(self):
        new_list = []
        for state in self.apta.G.nodes:
            if self.apta.is_red(state) and not self.apta.is_leaf(state):
                new_list.append(state)

        self.red_states = new_list
    def make_set_for_every_state_rooted_at(self, ds, s):
        ds.make_set(s)
        descendants = nx.descendants(self.apta.G, s)
        for d in descendants:
            ds.make_set(d)

    def compute_scour(self, ds):
        merging_scour = 0
        # states_before_merge = self.apta.G.number_of_nodes()
        # backup = copy.deepcopy(self.apta)
        # merge_sets(ds, self.apta)
        # states_after_merge = self.apta.G.number_of_nodes()
        # if states_before_merge != states_after_merge:
        #     merging_scour = states_before_merge - states_after_merge - 1
        # if has_negative_patterns(self.apta, self.negative_patterns, ds):
        #     print(f'Valid but incorrect merge: scour for {ds.s1} & {ds.s2}: {ds.merging_scour}')
        #     merging_scour = -2
        # self.apta = backup
        all_sets = ds.get_sets()
        # statesOfInterest=[]
        for representative, elements in all_sets.items():
            if len(elements) > 1:
                # statesOfInterest.append(representative)
                merging_scour += (len(elements) - 1)
        ds.merging_scour = merging_scour
        if merging_scour > -1:
            backup = copy.deepcopy(self.apta)
            merge_sets(ds, self.apta)
            # considering the new hypothesis
            statesOfInterest = []
            for state in self.apta.G.nodes:
                if self.apta.is_red(state):
                    statesOfInterest.append(state)
            has_negPat, selfloopCount, alternatingCount, nextCounter = has_negative_patterns(self.apta, self.negative_patterns, statesOfInterest)
            if has_negPat:
                # print(f'Valid but incorrect merge: scour for {ds.s1} & {ds.s2}: {ds.merging_scour}')
                merging_scour = -2
            self.apta = backup

            self.selfloppPat_rejectedCount+=selfloopCount
            self.alternatingPat_rejectedCount+=alternatingCount
            self.nextPat_rejectedCount+=nextCounter

        return merging_scour

    def compute_scour_with_positive_patterns(self, ds):
        merging_scour = 0
        states_before_merge = self.apta.G.number_of_nodes()
        properties_before_merge= getProperties(self.apta, self.all_properties)
        backup = copy.deepcopy(self.apta)
        merge_sets(ds, self.apta)
        states_after_merge = self.apta.G.number_of_nodes()
        properties_after_merge = getProperties(self.apta, self.all_properties)
        properties_scour = calculate_properties_scour(properties_before_merge, properties_after_merge, self.properties_average_scour)
        self.apta = backup
        if states_before_merge != states_after_merge:
            merging_scour = (states_before_merge - states_after_merge -1)+properties_scour
            # merging_scour = states_before_merge - states_after_merge - 1
        return merging_scour

    def compute_scour_with_negative_patterns(self, ds):
        merging_scour = 0
        states_before_merge = self.apta.G.number_of_nodes()
        # properties_before_merge= getProperties(self.apta, self.all_properties)
        backup = copy.deepcopy(self.apta)
        merge_sets(ds, self.apta)
        states_after_merge = self.apta.G.number_of_nodes()
        negPatterns_score= get_score_for_negative_patterns_in_hypo_automta(self.apta, self.negative_patterns)
        # properties_scour = calculate_properties_scour(properties_before_merge, properties_after_merge, self.properties_average_scour)
        self.apta = backup
        if states_before_merge != states_after_merge:
            merging_scour = (states_before_merge - states_after_merge -1)+negPatterns_score
            # merging_scour = states_before_merge - states_after_merge - 1
        return merging_scour

    def pick_high_scour_pair(self, list_of_mergable_states):# list of disjoint_sets object
        # Sort the list of lists based on the merging_scour (3rd item)
        list_of_mergable_states.sort(key=lambda x: x.merging_scour, reverse=True)

        # pick up the pair with the highest scour
        ds_with_highest_scour = list_of_mergable_states.pop(0)

        return ds_with_highest_scour

    def draw(self):
        self.apta.G.nodes[self.apta.root]['color'] = 'green'
        p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
        p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
        p.write_png(f'output/figure{FSM.figure_num:02d}.png')
        FSM.figure_num+=1

    def draw2(self, outputfile):
        temp_color = self.apta.G.nodes[self.apta.root]['fillcolor']
        self.apta.G.nodes[self.apta.root]['fillcolor'] = 'green'
        p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
        p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
        p.write_png(f'output/{outputfile}.png')
        FSM.figure_num+=1
        self.apta.G.nodes[self.apta.root]['fillcolor'] = temp_color

    def compute_classes2(self,ds ,work_to_do):
        add_something_new = False
        go_agin = False
        updated_work_to_do= work_to_do.copy()
        for represitative, set_to_merge in work_to_do.items():
            # set_to_merge is all states that need to merged together
            # set_to_merge = ds.get_set(red)
            checked_lables = []
            for s1 in set_to_merge:
                current_state_out_transitions = self.apta.get_out_edges(s1)
                other_state_out_transitions = self.get_other_state_out_transitions(s1, set_to_merge)
                for s1_trans in current_state_out_transitions:
                    label = self.apta.get_edge_label(s1_trans)
                    if label not in checked_lables:
                        checked_lables.append(label)
                        for other_state_out_trans in other_state_out_transitions:
                            if label == self.apta.get_edge_label(other_state_out_trans):
                                s1_target_state = s1_trans[1]
                                s2_target_state = other_state_out_trans[1]
                                add_something_new = ds.union(s1_target_state, s2_target_state)
                                updated_work_to_do[ds.find(s1_target_state)] = ds.get_set(s1_target_state)
                                # print(f'work_to_do: {work_to_do}')
                                if add_something_new:
                                    go_agin = True

        if go_agin:
            self.compute_classes2(ds, updated_work_to_do)

    def get_other_state_out_transitions(self, state, set_to_merge):
        # new_lst = set_to_merge.remove(state)
        out_transitions=[]
        for s in set_to_merge:
            s_out_trans = self.apta.get_out_edges(s)
            for out_trans in s_out_trans:
               out_transitions.append(out_trans)
        return out_transitions

    def print_pair_label(self, ds, mergeable_pairs, apta):

        # check if the states have different labels (incorrect merge)
        # this only works with labeled APTA (APTA where states have the same label as the reference automata)
        if (apta.get_state_reference_label(ds.s1) != apta.get_state_reference_label(ds.s2)):
            print(f'Incorrect merge:[{ds.s1}({apta.get_state_reference_label(ds.s1)}), {ds.s2}({apta.get_state_reference_label(ds.s2)}), {ds.merging_scour}]')
        else:
            print(f'Correct merge: [{ds.s1}({apta.get_state_reference_label(ds.s1)}), {ds.s2}({apta.get_state_reference_label(ds.s2)}), {ds.merging_scour}]')

        # sets = ds.get_sets()
        # for set in sets.items():
        #     target, merge_list = set
        #     if len(merge_list) > 1:
        #         # check if the states have different labels (incorrect merge)
        #         # this only works with labeled APTA (APTA where states have the same label as the reference automata)
        #         target_label = apta.get_state_reference_label(target)
        #         if any(apta.get_state_reference_label(state) != target_label for state in merge_list):
        #             print(f'Incorrect merge:{merge_list}')
        #             for ds_item in mergeable_pairs:
        #                 print(f'All pairs: [{ds_item.s1}({apta.get_state_reference_label(ds_item.s1)}), {ds_item.s2}({apta.get_state_reference_label(ds_item.s2)}), {ds_item.merging_scour}]')
        #         else:
        #             print(f'Correct merge: {merge_list}')
        #         for s in merge_list:
        #             print(f'-->[{apta.get_state_reference_label(s)}]')