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

    for line in f.readlines():
        color = ''
        shape = 'oval'
        x = line.split()
        frm, to, lbl = x[0], x[1], x[2]

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
    return G


def buildGraphFromMatrix(fname):
    # print('start')
    G = nx.MultiDiGraph()
    f = open(fname)
    alphabet = []
    for line in f.readlines():
        if line == "training positive:\n":
            break
        color = ''
        shape = 'oval'
        x = line.split()
        frm, to, lbl = x[0], x[1], x[2]

        if lbl not in alphabet:
            alphabet.append(lbl)

        if len(x) == 4:
            if x[3] == 'rejected':
                color = '#FA7E7E'
                ntype = 'rejected'
                shape = 'square'
            elif x[3] == 'accepted':
                color = 'lightblue'
                ntype = 'accepted'
                shape = 'doublecircle'
            else:
                color = 'white'
                ntype = 'unlabeled'
                shape = 'oval'

        ntype = 'unlabeled' if len(x) == 3 else x[3]
        G.add_node(frm, label=frm)
        # G.add_node(to, label=to)
        G.add_node(to, label=to, type=ntype, style='filled', fillcolor=color, shape=shape)
        G.add_edge(frm, to, label=lbl, weight='1')
        # print(frm, to, lbl)

    f.close()
    return G, alphabet

def build_adjs_matrix(input_file, counter):
    # open original file
    input = [l.strip().lower() for l in open(input_file).readlines()]

    # create file named "matrixOfRefrencedAuotmata.adjlist"
    # W: will overwirte any previous contents
    output_file = f'input/matrixOfRefrencedAuotmata{counter}.adjlist'
    f = open(output_file, "w")

    for line in input:
        if not line or line.strip().startswith("#") or line.strip() == '':
            continue
        elif line in ['postive sequences', 'positive sequences', 'negative sequences', 'numbre of transitions:']:
            break

        list = [l.strip().upper() for l in line.replace(' - ',',').replace(' -> ',',').split(',') if l != ""]
        # row = list[0].split('<', 1)[0] + ' ' +list[2].split('<', 1)[0] + ' ' + list[1] +'\n'
        row = list[0] + ' ' + list[1] + ' ' + list[2] + '\n'
        f.write(row)

    f.close()

    return output_file
def graph_to_string(graph):
    # create file named "matrixOfRefrencedAuotmata.adjlist"
    # W: will overwirte any previous contents
    f = open("input/LearnedAuotmata_string.txt", "w")

    for state in graph.nodes:
        out_edges = graph.out_edges(state, keys=True)
        for edge in out_edges:
            lbl = graph.get_edge_data(edge[0], edge[1], edge[2])["label"]
            row = f'{edge[0]}-{lbl}->{edge[1]}\n'
            f.write(row)

    f.close()

def draw(G, filename):
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png(filename)


if __name__ == '__main__':
    # clean_folder()
    build_adjs_matrix('input/PosNegExamples.txt')
    #test_solve determinism
    G = read_matrix('input/matrixOfRefrencedAuotmata.adjlist')
    draw(G, "output/RefrencedAuotmata.png")
