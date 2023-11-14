from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.PatternsChecker import *
from PattrenFromTraces.matrix_reader import *
if __name__ == '__main__':
    G = read_matrix('TestCases/findEventuallyInG/FSM.adjlist')
    draw(G, "TestCases/findEventuallyInG/expected_graph/targetFSM.png")
    apta = APTA()
    apta.G = G
    print(has_Eventually(apta, 'L0', 'L1'))