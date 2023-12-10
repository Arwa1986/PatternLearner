import os
import shutil
import networkx as nx

def clean_folder():
    folder = 'output'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def read_matrix(fname):
    # print('start')
    G = nx.MultiDiGraph()
    f = open(fname)
    alphabet = []
    for line in f.readlines():
        color = ''
        shape = 'oval'
        x = line.split()
        frm, to, lbl = x[0], x[1], x[2]
        if lbl not in alphabet:
            alphabet.append(lbl)
        if len(x)==4:
            if    x[3] == 'rejected':
                color = '#FA7E7E'
                ntype = 'rejected'
                shape = 'square'
            elif  x[3] == 'accepted':
                color = 'lightblue'
                ntype = 'accepted'
                shape = 'doublecircle'
            else:
                color = 'white'
                ntype = 'unlabeled'
                shape = 'oval'

        ntype = 'unlabeled' if len(x)==3 else x[3]
        G.add_node(frm, label=frm)
        # G.add_node(to, label=to)
        G.add_node(to, label=to, type=ntype, style='filled', fillcolor=color, shape=shape)
        G.add_edge(frm, to, label=lbl, weight='1')
        # print(frm, to, lbl)

    f.close()

    # print('done')
    return G, alphabet



def draw(G, filename):
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png(filename)


if __name__ == '__main__':
    # clean_folder()

    #test_solve determinism
    G, alphabet = read_matrix('TestCases/findAlternatingInG/FSM.adjlist')
    print(f'Alphabet: {alphabet}')
    draw(G, "TestCases/findAlternatingInG/expected_graph/targetFSM.png")
