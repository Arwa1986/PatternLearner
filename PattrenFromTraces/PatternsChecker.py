from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.TemporalPeoperty import TemporalProperty
from PattrenFromTraces.matrix_reader import *

def has_selfloop(apta, label):
    found= False
    selfloops = apta.get_self_loop()
    for sl in selfloops:
        if sl[-1] == label:
            found = True
        else:
            found =  False
    return found

def get_negative_selfloop(DFA, label):
    # list of states' number in which a negative patterns occurs
    # states_with_selfloop = [node for node in DFA.G.nodes() if
    #                         DFA.G.has_edge(node, node) and DFA.G[node][node].get('label') == label]
    # return states_with_selfloop
    selfloops = DFA.get_self_loop()
    states_with_selfloop = []
    for sl in selfloops:
        if sl[-1] == label:
            states_with_selfloop.append(sl[0])
    return states_with_selfloop

def has_Alternating(apta:APTA, event1, event2, statesOfInterest):
    found=False
    all_event1_edges = get_edges_with_label2(apta.G, event1, statesOfInterest)
    all_event2_edges = get_edges_with_label2(apta.G, event2, statesOfInterest)
    for event1_edge in all_event1_edges:
        for event2_edge in all_event2_edges:
            #if event1's source is the target for event2
            # and event1#s target is the source of event2
            if event1_edge[0] == event2_edge[1] and event1_edge[1] == event2_edge[0]:
                found=True
    return found
def get_negative_alternating(DFA, event1, event2):
    alternating_pairs=[]
    all_event1_edges = get_edges_with_label(DFA.G, event1)
    all_event2_edges = get_edges_with_label(DFA.G, event2)
    for event1_edge in all_event1_edges:
        for event2_edge in all_event2_edges:
            # if event1's source is the target for event2
            # and event1#s target is the source of event2
            if event1_edge[0] == event2_edge[1] and event1_edge[1] == event2_edge[0]:
                alternating_pairs.append([event1_edge[0], event1_edge[1]])

    return alternating_pairs


def get_edges_with_label(graph, label):
    edges = [edge for edge in graph.edges(data=True) if edge[2].get('label') == label]
    return edges

def get_edges_with_label2(graph, label, statesOfInterset):
    if statesOfInterset:
        # get all out_edges with a specific label for every item in statesOfInterset
        edges = [edge for edge in graph.out_edges(statesOfInterset, data='label') if edge[2]==label]
    else:
        # get all out_edges with a specific label for all states in the graph
        edges = [edge for edge in graph.out_edges(data='label') if edge[2] == label]
    return edges

def has_Eventually(apta, event1, event2):
    found = False
    selfloops = apta.get_self_loop()
    for sl in selfloops:
        if sl[-1] == event1:
            outEdges = apta.get_out_edges(sl[0])
            for edge in outEdges:
                label = apta.get_edge_label(edge)
                if label == event2:
                    found=True
    return found

def getProperties(apta, all_properties):
    existed_properties = []
    for tp in all_properties:
        tp_exist = False
        if tp.pattern == 'Selfloop':
            # check if it has selfloop for event1
            tp_exist = has_selfloop(apta, tp.event1)
        elif tp.pattern == 'Alternating':
            # check if it has pattern for event1 & event2
            tp_exist = has_Alternating(apta, tp.event1, tp.event2)
        elif tp.pattern == 'Eventually':
            # check if it has pattern for event1
            tp_exist = has_Eventually(apta, tp.event1, tp.event2)

        if tp_exist:
            existed_properties.append(tp)
    return existed_properties
def calculate_properties_scour(properties_before_merge, properties_after_merge, properties_average_scour):
    # for each lost property:
    #   decrease scour by 2 if important
    #   decrease scour by 1 in not important
    # for each gained property:
    #   increase scour by 2 if important
    #   increase scour by 1 in not important
    scour =0
    # print(f'LOST:')
    for before in properties_before_merge:
        if before not in properties_after_merge:
            if before.get_weigth() >= properties_average_scour:
                # important property is lost
                scour -= 2
            else:
                # unimportant property is lost
                scour -= 1
            # before.print()
    # print(f'GAINED:')
    for after in properties_after_merge:
        if after not in properties_before_merge:
            if after.get_weigth() >= properties_average_scour:
                # important property is gained
                scour += 2
            else:
                # unimportant property is gained
                scour += 1
            # after.print()
    return scour


if __name__ == '__main__':
    G = read_matrix('TestCases/findEventuallyInG/FSM.adjlist')
    draw(G, "TestCases/findEventuallyInG/expected_graph/targetFSM.png")
    apta = APTA()
    apta.G = G
    # print(has_Eventually(apta, 'L0', 'L1'))
    tp1 = TemporalProperty('L1', 'L0')
    tp1.pattern = 'Alternating'
    tp1.counter = 9

    tp2 = TemporalProperty('L2', 'L0')
    tp2.pattern = 'Selfloop'
    tp2.counter = 8

    tp3 = TemporalProperty('L1', 'L2')
    tp3.pattern = 'Alternating'
    tp3.counter = 10

    tp4 = TemporalProperty('L2', 'L1')
    tp4.pattern = 'Alternating'
    tp4.counter = 3

    tp5 = TemporalProperty('L1', 'L0')
    tp5.pattern = 'Selfloop'
    tp5.counter = 4

    tp6 = TemporalProperty('L1', 'L0')
    tp6.pattern = 'Alternating'
    tp6.counter = 9

    tp7 = TemporalProperty('L2', 'L1')
    tp7.pattern = 'Alternating'
    tp7.counter = 3

    avgScour = (9+8+10+3+4)/5
    print(f'average scour: {avgScour}')
    before_merge_properties = [tp1, tp2, tp3, tp4]
    after_merge_properties = [tp6, tp7, tp5]
    scour = calculate_properties_scour(before_merge_properties, after_merge_properties , avgScour)
    print(scour)

# if __name__ == '__main__':
#     G = read_matrix('TestCases/findEventuallyInG/FSM.adjlist')
#     draw(G, "TestCases/findEventuallyInG/expected_graph/targetFSM.png")
#     apta = APTA()
#     apta.G = G
#     print(has_Eventually(apta, 'L0', 'L1'))
#     tp1 = TemporalProperty('L1', 'L0')
#     tp1.pattern = 'Alternating'
#     tp1.counter = 9
#
#     tp2 = TemporalProperty('L2', 'L0')
#     tp2.pattern = 'Selfloop'
#     tp2.counter = 8
#
#     tp3 = TemporalProperty('L1', 'L2')
#     tp3.pattern = 'Alternating'
#     tp3.counter = 10
#
#     tp4 = TemporalProperty('L2', 'L1')
#     tp4.pattern = 'Alternating'
#     tp4.counter = 3
#
#     tp5 = TemporalProperty('L1', 'L0')
#     tp5.pattern = 'Selfloop'
#     tp5.counter = 4
#
#     all_properties = [tp1, tp2, tp3, tp4]
#
#     exsiting_properties = getProperties(apta, all_properties)
#     for p in exsiting_properties:
#         p.print()
#
