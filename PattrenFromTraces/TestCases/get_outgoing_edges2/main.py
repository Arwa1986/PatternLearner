from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.PatternsChecker import get_edges_with_label2
from PattrenFromTraces.matrix_reader import *

if __name__ == '__main__':
    graph = read_matrix('FSM.adjlist')
    draw(graph, "expected_graph/targetFSM.png")
    states = ['1','2']
    label = 'L1'
    # apta = APTA()
    # apta.G = G
    # print(get_edges_with_label2(G, 'L1', ['1','2','3']))

    # get all out_edges for every item in states:
    # edges = graph.out_edges(states, data= 'label')

    # get all out_edges with a specific label for every item in states
    edges = [edge for edge in graph.out_edges(states, data='label') if edge[2]==label]

    # get all out_edges with a specific label for all states in the graph
    # edges = [edge for edge in graph.out_edges(data='label') if edge[2] == label]
    print(edges)