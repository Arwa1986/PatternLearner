import networkx as nx

from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.PatternsChecker import get_negative_selfloop

if __name__ == '__main__':
    graph = nx.MultiDiGraph()
    graph.add_edge(1, 1, label='A')
    graph.add_edge(2, 2, label='B')
    graph.add_edge(3, 3, label='A')
    graph.add_edge(4, 4, label='C')
    graph.add_edge(5, 5, label='B')
    apta = APTA()
    apta.G = graph
    print(get_negative_selfloop(apta, 'B'))