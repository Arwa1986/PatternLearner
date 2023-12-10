from APTA import APTA
from FSM import FSM
from PattrenFromTraces.SatPatterns_RandFSM import discover_patterns_fromTraces
from PattrenFromTraces.evaluation import Evaluation
from input_reader2 import import_input, clean_folder

if __name__ == '__main__':
    clean_folder()
    # accepted_traces, rejected_traces= import_input("input/PosNegExamples.txt")
    traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp  = import_input("input/traces.txt")
    print(f'..........Training.............')
    print(f'number of Positive Examples: {len(traningPosExmp)}')
    print(f'number of Negative Examples: {len(trainingNegExmp)}')

    # building the tree
    apta = APTA()
    apta.build_APTA(traningPosExmp, trainingNegExmp)

    alphabet = apta.alphabet
    print(f'Alphabet: {alphabet}')
    extraced_properties, average_weigth = discover_patterns_fromTraces(traningPosExmp, alphabet)

    fsm = FSM(apta, extraced_properties, average_weigth)
    fsm.run_EDSM_learner()

    print(f'...............EVALUATION................')
    print(f'number of Positive Examples: {len(evalPosExmp)}')
    print(f'number of Negative Examples: {len(evalNegExamp)}')
    eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
    eval.evaluate()