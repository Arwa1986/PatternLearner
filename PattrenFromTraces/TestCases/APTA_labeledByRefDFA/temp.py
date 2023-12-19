import networkx as nx


def draw_multiDigraph(G):
    p = nx.nx_agraph.pygraphviz_layout(G, prog='dot')
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png(f'figure.png')

if __name__ == '__main__':
    G = nx.MultiGraph()
    G.add_node('A',Label='A')
    G.add_node('2', Label='B')
    G.add_node(3)
    G.add_node('4')
    G.add_edge('A','2', Label='a')
    G.add_edge('2', '4', Label='b')
    draw_multiDigraph(G)