import copy
apta = None
def merge_sets(ds, aptaObj):
    global apta
    apta = aptaObj
    sets = ds.get_sets()
    for set in sets.items():
        represinitive, states = set
        if len(states)>1:
            merge_states(represinitive, states)

def merge_states(target, merge_list):
    global apta
    list_type = get_list_type(merge_list)
    if any (apta.get_color(state) == 'red' for state in merge_list):
        apta.set_color(target, 'red')
    merge_list.remove(target)

    for i in range(0, len(merge_list)):
        source = merge_list[i]
        transfer_out_edge(source, target)
        transfer_in_coming_edges(source, target)

        if source == apta.root:
            apta.root = target
        if source != target:  # this if to solve butterfly problem
            apta.delete_state(source)
        apta.set_state_type(target,list_type)
    return target

def get_list_type(merge_list):
    _c, typ = is_compatible_type(merge_list)
    return typ
 # is_compatible_type: boolean
    # return true is s1 and s2 of the same type or at least of them is unlabeled
    # return false if one is rejected the other is accepted

def is_compatible_type(list):
    global apta
    compatible = False
    list_type = 'unlabeled'
    if any (apta.get_state_type(state) == 'rejected' for state in list):
        if any(apta.get_state_type(state) == 'accepted' for state in list):
            # some rejected and some accepted
            compatible = False
        else: # at least one is rejected and all other are unlabeled
            compatible = True
            list_type = 'rejected'
    elif any(apta.get_state_type(state) == 'accepted' for state in list):
        # some are accepted and non are rejected
        list_type = 'accepted'
        compatible = True
    else:
        # all unlabeled
        compatible = True
        list_type = 'unlabeled'

    return compatible, list_type
def transfer_out_edge( source, target):
    global apta
    if source == target:
        return
    # mylist is temp list to make a copy of the out_edges list
    source_out_edges = copy.deepcopy(apta.get_out_edges(source))

    for e in source_out_edges:
        target_out_edges = copy.deepcopy(apta.get_out_edges(target))
        if is_in_target_out_edges(e, target_out_edges):
            continue
        temp_lbl = apta.get_edge_label(e)
        apta.delete_edge(e)
        # if the edge is a self loop in the source state move it to the target state
        if e[0] == e[1]:
            apta.add_edge(target, target, temp_lbl)

        else:
            apta.add_edge(target, e[1], temp_lbl)

def is_in_target_out_edges(edge_tuple, edges_list):
    global apta
    for e in edges_list:
        # if both edges have the same label
        if apta.get_edge_label(e) == apta.get_edge_label(edge_tuple):
            return True
    return False

def transfer_in_coming_edges(source, target):
    global apta
    copylist = copy.deepcopy(apta.get_in_edges(source))

    for e in copylist:
        temp_lbl = apta.get_edge_label(e)
        if not apta.has_in_edge(target, e):
            apta.add_edge(e[0], target, temp_lbl)
        apta.delete_edge(e)


def is_valid_merge(aptaObj, ds):
    global apta
    apta = aptaObj
    all_sets = ds.get_sets()
    for representative, _set in all_sets.items():
        compatible, list_type = is_compatible_type(_set)
        if not compatible:
            return False
    return True