from PattrenFromTraces.APTA_labeledBYRefDFA import APTA2
from PattrenFromTraces.APTA import APTA
# from PattrenFromTraces.FSM import FSM
# from PattrenFromTraces.SatPatterns_RandFSM import discover_patterns_fromTraces
# from PattrenFromTraces.evaluation import Evaluation
# from evaluation import Evaluation
# from input_reader2 import import_input, clean_folder
# from PattrenFromTraces.input_reader import *
from PattrenFromTraces.matrix_reader import *
def get_reference_DFA():
    # build_adjs_matrix('PosNegExamples.txt')
    G, alphabet = read_matrix2('matrixOfRefrencedAuotmata.adjlist')
    draw(G, "RefrencedAuotmata.png")

    apta_obj = APTA()
    apta_obj.G = G
    apta_obj.root = 'A'
    apta_obj.alphabet = alphabet
    return apta_obj

if __name__ == '__main__':
    # clean_folder()
    reference_DFA = get_reference_DFA()
    # accepted_traces, rejected_traces= import_input("PosNegExamples.txt")
    # traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp  = import_input("input/PosNegExamples.txt")
    # print(f'..........Training.............')
    # print(f'number of Positive Examples: {len(traningPosExmp)}')
    # print(f'number of Negative Examples: {len(trainingNegExmp)}')

    # building the tree
    apta = APTA2(reference_DFA)
    apta.build_APTA([['a','b','a'],['a', 'a'],['a','b','b']], [])
    apta.draw_multiDigraph()
    # apta.build_APTA(traningPosExmp, trainingNegExmp)
    #
    # alphabet = apta.alphabet
    # print(f'Alphabet: {alphabet}')
    # extraced_properties, average_weigth = discover_patterns_fromTraces(traningPosExmp, alphabet)
    # extraced_properties, average_weigth = discover_patterns_fromTraces(accepted_traces, alphabet)

    # fsm = FSM(apta, extraced_properties, average_weigth, reference_DFA)
    # fsm.run_EDSM_learner()

    # print(f'...............EVALUATION................')
    # print(f'number of Positive Examples: {len(evalPosExmp)}')
    # print(f'number of Negative Examples: {len(evalNegExamp)}')
    # eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
    # eval.evaluate()