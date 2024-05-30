from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.APTA_labeledBYRefDFA import LabeledAPTA
from PattrenFromTraces.FSM import FSM
from PattrenFromTraces.SatPatterns_RandFSM import discover_patterns_fromTraces
from PattrenFromTraces.evaluation import Evaluation
# from evaluation import Evaluation
from PattrenFromTraces.input_reader import GetTrainingEvaluationData
from PattrenFromTraces.matrix_reader import *
import csv

def get_reference_DFA(input_file, counter):
    G, alphabet = buildGraphFromMatrix(input_file)
    draw(G, f"output/RefrencedAuotmata{counter}.png")

    apta_obj = APTA()
    apta_obj.G = G
    apta_obj.root = 'V0'
    apta_obj.alphabet = alphabet
    return apta_obj

if __name__ == '__main__':
        # clean_folder()
        # input_file_path='input-10states/automata69.txt'
        # reference_DFA = get_reference_DFA(input_file_path, 1)
        # traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp = GetTrainingEvaluationData(input_file_path)
        # LabeledAPTA = LabeledAPTA(reference_DFA)
        # LabeledAPTA.build_APTA(traningPosExmp, trainingNegExmp)
        # LabeledAPTA.draw_multiDigraph()
        #
        # apta = APTA()
        # apta.G = LabeledAPTA.G
        # apta.root = 0
        # apta.alphabet = LabeledAPTA.alphabet
        #
        # fsm = FSM(apta, [], 0, reference_DFA)
        # fsm.run_EDSM_learner()
        # fsm.draw()
        # print(f'number of rejected selfloop patterns: {fsm.selfloppPat_rejectedCount}')
        # print(f'number of rejected alternating patterns: {fsm.alternatingPat_rejectedCount}')
        # print(f'number of rejected next patterns: {fsm.nextPat_rejectedCount}')
        #
        # eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
        # true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, BCR, Accuracy= eval.evaluate()
        # print(f'F_measure (2 patterns)= {F_measure}')

# if __name__ == '__main__':
#     clean_folder()
#     input_file_path='input-10states/automata74.txt'
#     reference_DFA = get_reference_DFA(input_file_path, 1)
#     traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp = GetTrainingEvaluationData(input_file_path)
#     LabeledAPTA = LabeledAPTA(reference_DFA)
#     LabeledAPTA.build_APTA(traningPosExmp, trainingNegExmp)
#     LabeledAPTA.draw_multiDigraph()
#
#     apta = APTA()
#     apta.G = LabeledAPTA.G
#     apta.root = 0
#     apta.alphabet = LabeledAPTA.alphabet
#
#     fsm = FSM(apta, [], 0, reference_DFA)
#     fsm.run_EDSM_learner()
#     fsm.draw()
#     eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
#     true_positive, true_negative, false_positive, false_negative, precision, recall, F_measure, Accuracy = eval.evaluate()
#     print(f'F_measure= {F_measure}')

    # form input folder
    # for each file in input_folder:
        # get refrence automata
        # get training/ elavuation data
        # start learner
            # build APTA
            # run_learner
        # save learnt model
        # evaluate
        # save result

    clean_folder()
    input_folder = "input-10states"
    counter = 1
    # inputfile = "input/PosNegExamples.txt"

    selfloppPat_rejectedCount=0
    alternatingPat_rejectedCount=0
    nextPat_rejectedCount=0
    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)

        reference_DFA = get_reference_DFA(input_file_path, counter)
        traningPosExmp, trainingNegExmp, evalPosExmp, evalNegExamp  = GetTrainingEvaluationData(input_file_path)

        # building the tree
        apta = APTA()
        apta.build_APTA(traningPosExmp, trainingNegExmp)
        fsm = FSM(apta, [], 0, reference_DFA)
        fsm.run_EDSM_learner()
        # fsm.draw2(f'automata{counter}')

        eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
        true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, BCR, Accuracy = eval.evaluate()

        data = [
            [file_name, len(traningPosExmp), len(trainingNegExmp), len(evalPosExmp), len(evalNegExamp),
             true_positive, true_negative, false_positive, false_negative, precision, recall, specificity,
             F_measure,BCR, Accuracy]]
        file_path = 'NegPat10States200trace3NegPat.csv'
        # Write data to CSV file
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f'Automata{counter}')
        counter += 1

        selfloppPat_rejectedCount+=fsm.selfloppPat_rejectedCount
        alternatingPat_rejectedCount+=fsm.alternatingPat_rejectedCount
        nextPat_rejectedCount+=fsm.nextPat_rejectedCount
    print(f'number of rejected selfloop patterns: {selfloppPat_rejectedCount}')
    print(f'number of rejected alternating patterns: {alternatingPat_rejectedCount}')
    print(f'number of rejected next patterns: {nextPat_rejectedCount}')

    # building the tree
    # apta = APTA()
    # apta.build_APTA(accepted_traces, rejected_traces)
    # apta.draw_multiDigraph()
    # apta.build_APTA(traningPosExmp, trainingNegExmp)
    # LabeledAPTA = APTA2(reference_DFA)
    # # LabeledAPTA.build_APTA(accepted_traces, rejected_traces)
    # LabeledAPTA.build_APTA(traningPosExmp, trainingNegExmp)
    # LabeledAPTA.draw_multiDigraph()

    # alphabet = apta.alphabet
    # print(f'Alphabet: {alphabet}')
    # extraced_properties, average_weigth = discover_patterns_fromTraces(traningPosExmp, alphabet)
    # extraced_properties, average_weigth = discover_patterns_fromTraces(accepted_traces, alphabet)

    # fsm = FSM(apta, extraced_properties, average_weigth, reference_DFA)
    # fsm = FSM(apta, [], 0, reference_DFA)
    # fsm.run_EDSM_learner()

    # print(f'...............EVALUATION................')
    # print(f'number of Positive Examples: {len(evalPosExmp)}')
    # print(f'number of Negative Examples: {len(evalNegExamp)}')
    # eval = Evaluation(fsm, evalPosExmp, evalNegExamp)
    # eval.evaluate()
    # print(f'root: {fsm.apta.root}')