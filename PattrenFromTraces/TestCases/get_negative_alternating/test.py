import networkx as nx

from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.PatternsChecker import get_negative_alternating

if __name__ == '__main__':
    graph = nx.MultiDiGraph()
    graph.add_edge(1, 2, label='A')
    graph.add_edge(2, 1, label='B')
    graph.add_edge(3, 5, label='A')
    graph.add_edge(4, 4, label='C')
    graph.add_edge(5, 3, label='B')
    apta = APTA()
    apta.G = graph
    print(get_negative_alternating(apta, 'B','A'))