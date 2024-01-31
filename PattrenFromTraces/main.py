from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.APTA_labeledBYRefDFA import APTA2
from PattrenFromTraces.FSM import FSM
from PattrenFromTraces.SatPatterns_RandFSM import discover_patterns_fromTraces
from PattrenFromTraces.evaluation import Evaluation
# from evaluation import Evaluation
from input_reader2 import import_input, clean_folder
# from input_reader import *
from PattrenFromTraces.matrix_reader import *
def get_reference_DFA():
    build_adjs_matrix('input/PosNegExamples.txt')
    G, alphabet = read_matrix2('input/matrixOfRefrencedAuotmata.adjlist')
    draw(G, "output/RefrencedAuotmata.png")

    apta_obj = APTA()
    apta_obj.G = G
    apta_obj.root = 'V0'
    apta_obj.alphabet = alphabet
    return apta_obj

if __name__ == '__main__':
    clean_folder()
    reference_DFA = get_reference_DFA()
    # accepted_traces, rejected_traces= import_input("input/PosNegExamples2.txt")
    traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp  = import_input("input/traces.txt")
    print(f'..........Training.............')
    print(f'number of Positive Examples: {len(traningPosExmp)}')
    print(f'number of Negative Examples: {len(trainingNegExmp)}')

    # building the tree
    apta = APTA()
    # apta.build_APTA(accepted_traces, rejected_traces)
    # apta.draw_multiDigraph()
    apta.build_APTA(traningPosExmp, trainingNegExmp)
    # LabeledAPTA = APTA2(reference_DFA)
    # # LabeledAPTA.build_APTA(accepted_traces, rejected_traces)
    # LabeledAPTA.build_APTA(traningPosExmp, trainingNegExmp)
    # LabeledAPTA.draw_multiDigraph()

    # alphabet = apta.alphabet
    # print(f'Alphabet: {alphabet}')
    # extraced_properties, average_weigth = discover_patterns_fromTraces(traningPosExmp, alphabet)
    # extraced_properties, average_weigth = discover_patterns_fromTraces(accepted_traces, alphabet)

    # fsm = FSM(apta, extraced_properties, average_weigth, reference_DFA)
    fsm = FSM(apta, [], 0, reference_DFA)
    fsm.run_EDSM_learner()

    print(f'...............EVALUATION................')
    print(f'number of Positive Examples: {len(evalPosExmp)}')
    print(f'number of Negative Examples: {len(evalNegExamp)}')
    eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
    eval.evaluate()
    print(f'root: {fsm.apta.root}')