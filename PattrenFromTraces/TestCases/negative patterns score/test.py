from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.matrix_reader import *
from PattrenFromTraces.negative_patterns2 import *

if __name__ == '__main__':
    build_adjs_matrix('PosNegExamples.txt')

    G, alphabet = read_matrix2('input/matrixOfRefrencedAuotmata.adjlist')
    draw(G, "RefrencedAuotmata.png")

    Referenced_DFA = APTA()
    Referenced_DFA.G = G
    Referenced_DFA.root = 'V0'
    Referenced_DFA.alphabet = alphabet

    print(f'Negative Patterns in Refrenced DFA: ')
    negative_pattern_referenced_DFA= get_negative_patterns(Referenced_DFA)


    # HYPOTHESIS AUTOMATA
    HG, Halphabet = read_matrix2('matrixOfHypoAuotmata.adjlist')
    draw(HG, "HypoAuotmata.png")

    Hypo_DFA = APTA()
    Hypo_DFA.G = HG
    Hypo_DFA.root = 'V0'
    Hypo_DFA.alphabet = Halphabet
    print(f'Negative Patterns found in Hypothesis DFA: ')
    get_score_for_negative_patterns_in_hypo_automta(Hypo_DFA, negative_pattern_referenced_DFA)
