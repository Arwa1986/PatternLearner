import unittest
from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.PatternsChecker import has_next
from PattrenFromTraces.matrix_reader import buildGraphFromMatrix,draw

class TestGraphsEquality(unittest.TestCase):
    def setUp(self):
        # referenceDFA = get_reference_DFA('referenceDFA.adjlist', 0, '1')
        # get the reference DFA
        input_file = 'referenceDFA.adjlist'
        root = '1'
        counter = 0
        G, alphabet = buildGraphFromMatrix(input_file)
        draw(G, f"RefrencedAuotmata{counter}.png")

        apta_obj = APTA()
        apta_obj.G = G
        apta_obj.root = root
        apta_obj.alphabet = alphabet
        self.referenceDFA = apta_obj

        self.expected_positive_next_pattern = [['open', 'edit'],
                                          ['open', 'exit'],
                                          ['edit', 'edit'],
                                          ['edit', 'save'],
                                          ['save', 'edit'],
                                          ['save', 'exit'],
                                          ['exit', 'open']]

        self.expected_negative_next_patterns = [['open', 'open'],
                                           ['open', 'save'],
                                           ['edit', 'open'],
                                           ['edit', 'exit'],
                                           ['save', 'open'],
                                           ['save', 'save'],
                                           ['exit', 'edit'],
                                           ['exit', 'save'],
                                           ['exit', 'exit']]

    def test_next_pattern(self):
        actual_positive_next_pat = []
        actual_negative_next_pat = []
        for i in range(len(self.referenceDFA.alphabet)):
            for j in range(len(self.referenceDFA.alphabet)):
                event1 = self.referenceDFA.alphabet[i]
                event2 = self.referenceDFA.alphabet[j]

                if has_next(self.referenceDFA, event1, event2):
                    actual_positive_next_pat.append([event1, event2])
                else:
                    actual_negative_next_pat.append([event1, event2])

        self.assertCountEqual(actual_positive_next_pat, self.expected_positive_next_pattern)
        self.assertCountEqual(actual_negative_next_pat, self.expected_negative_next_patterns)
if __name__ == '__main__':
    unittest.main()