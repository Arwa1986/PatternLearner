from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.matrix_reader import *
from PattrenFromTraces.PatternsChecker import *

def get_negative_patterns(apta_obj):
    # print(f'Negative Patterns in Refrenced DFA: ')
    alphabet  = apta_obj.alphabet
    negative_patterns = []
    for char in alphabet:
        if not has_selfloop(apta_obj, char):
            tp = TemporalProperty(char, '', 'Selfloop')
            negative_patterns.append(tp)

    for i in  range(len(alphabet)-1):
        for j in range(i+1, len(alphabet)):
            event1 = alphabet[i]
            event2 = alphabet[j]
            # alphabet, event1, even2 = pick_random_events(alphabet)
            if not has_Alternating(apta_obj, event1, event2, []):
                tp = TemporalProperty(event1, event2, 'Alternating')
                negative_patterns.append(tp)

    # for tp in negative_patterns:
    #     tp.print()

    return negative_patterns

def get_score_for_negative_patterns_in_hypo_automta(hypo_apta, negative_patterns):
    print(f'Negative Patterns found in Hypothesis DFA: ')
    score = 0
    for tp in negative_patterns:
        if tp.pattern == 'Selfloop':
            if has_selfloop(hypo_apta, tp.event1):
                tp.print()
                score -= 1
                locations_neg_selfloop= get_negative_selfloop(hypo_apta, tp.event1)
        elif tp.pattern == 'Alternating':
            if has_Alternating(hypo_apta, tp.event1, tp.event2):
                tp.print()
                score -= 2
        # elif tp.pattern == 'Eventually':
        #     tp.print()
        #     score -= 3
    return score

def has_negative_patterns(hypo_apta, negative_patterns, statesOfInterest):
    # print(f'Negative Patterns found in Hypothesis DFA: ')
    found_negative_patterns=False
    for tp in negative_patterns:
        if tp.pattern == 'Selfloop':
            if has_selfloop(hypo_apta, tp.event1):
                # tp.print()
                found_negative_patterns = True
                # locations_neg_selfloop= get_negative_selfloop(hypo_apta, tp.event1)
        elif tp.pattern == 'Alternating':
            if has_Alternating(hypo_apta, tp.event1, tp.event2, statesOfInterest):
                # tp.print()
                found_negative_patterns= True
        # elif tp.pattern == 'Eventually':
        #     tp.print()
        #     score -= 3
    return found_negative_patterns
if __name__ == '__main__':
    pass