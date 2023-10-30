def lost_selfloop(label):
    # use apta.get_self_loop

    # list_2: get selfloops after the merge
    # compare both list
    #     if label in list_1 but not in list_2
    #       return true
    # return false
    pass
def has_selfloop(label):
    selfloops = self.apta.get_self_loop()
    for sl in list_of_selfloop:
        if sl[-1] == label:
        return True
    else:
        return False
def obtain_selfloop(label):
    # use apta.get_self_loop
    # list_2: get selfloops after the merge
    # compare both list
    #     if label in list_2 but not in list_1
    #       return true
    # return false
    pass

def obtain_alternating(event1, event2):
    # for state in G:
    #   if state has outgoing transition with event1:
    #           e1_target = get the target state
    #           if e1_target state has outgoing transition with event2
    #                  e2_target = get the target state
    #                   if the e2_target == state
    #                       return True
    # return False
    pass

def obtain_eventually(event1, event2):
    pass