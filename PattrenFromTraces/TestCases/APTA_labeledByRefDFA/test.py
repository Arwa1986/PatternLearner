#
# # NOT Compelete
#
import unittest
#
from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.comapre_graphs import Graph_comparision
from PattrenFromTraces.APTA_labeledBYRefDFA import LabeledAPTA
from PattrenFromTraces.main import get_reference_DFA
from PattrenFromTraces.matrix_reader import *
from PattrenFromTraces.FSM import FSM
class TestGraphsEquality(unittest.TestCase):
    def test_APTA_accepted_and_unlabeled_staes(self):
        G1, _ = buildGraphFromMatrix('expected_APTA1.adjlist')
        expected_result = APTA()
        expected_result.G = G1
        expected_result.root = 'A'
        # fsm1 = FSM(expected_result,[],0,[])

        reference_DFA = get_reference_DFA("matrixOfRefrencedAuotmata.adjlist",0)
        reference_DFA.root = '0'

        # building the tree
        acctual_labeledAPTA = LabeledAPTA(reference_DFA)
        acctual_labeledAPTA.build_APTA([['a', 'b', 'a'], ['a', 'a'], ['a', 'b', 'b']], [])
        acctual_labeledAPTA.draw_multiDigraph()

        # convert from apta2 obj to apta object
        # because FSM accept apta obj only
        apta = APTA()
        apta.G = acctual_labeledAPTA.G
        apta.root = acctual_labeledAPTA.root
        # fsm2 = FSM(apta,[],0,[])

        # GC = Graph_comparision()
        # result = GC.are_graphs_equal(fsm1, fsm2)
        # self.assertTrue(result)

        state_label = 'A'
        self.assertTrue(apta.get_state_label(apta.root),state_label)

if __name__ == '__main__':
    unittest.main()

# if __name__ == '__main__':
#         G1, _ = buildGraphFromMatrix('expected_APTA1.adjlist')
#         expected_result = APTA()
#         expected_result.G = G1
#         expected_result.root = '0'
#         # fsm1 = FSM(expected_result,[],0,[])
#
#         reference_DFA = get_reference_DFA("matrixOfRefrencedAuotmata.adjlist",0)
#         reference_DFA.root = '0'
#
#         # building the tree
#         acctual_labeledAPTA = LabeledAPTA(reference_DFA)
#         acctual_labeledAPTA.build_APTA([['a', 'b', 'a'], ['a', 'a'], ['a', 'b', 'b']], [])
#         acctual_labeledAPTA.draw_multiDigraph()
#
#         # convert from apta2 obj to apta object
#         # because FSM accept apta obj only
#         apta = APTA()
#         apta.G = acctual_labeledAPTA.G
#         apta.root = acctual_labeledAPTA.root
#
#         for s in apta.G.nodes:
#             print(f'{s}: {apta.get_state_label(s)}')
