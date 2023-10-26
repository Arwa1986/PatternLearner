import random
from TemporalPeoperty import TemporalProperty
import re

properties = []

def run_(Positive_traces, alphabet):
    while alphabet:
        event1, event2 = pick_random_events(alphabet)

        patterns = ['Selfloop', 'Alternating', 'Eventually']
        for patrn in patterns:
            calculate_satisfactory(event1, event2, Positive_traces, patrn)
            calculate_satisfactory(event2, event1, Positive_traces, patrn)

def pick_random_events(alphabet):
    # Pick a random state from the list
    e1 = random.choice(alphabet)
    alphabet.remove(e1)
    e2 = random.choice(alphabet)
    alphabet.remove(e2)
    return e1, e2

def calculate_satisfactory(event1, event2, traces, patrn):
    tp = TemporalProperty(event1,event2)
    tp.pattern = patrn
    print(f'Pattern: {patrn}')
    print(f'Satisfied Traces:')
    for trace in traces:
        if satisfied(tp, trace):
            tp.counter+=1
            print(trace)
    tp.calculate_ratio(len(traces))
    tp.print()

def satisfied(tp, trace):
    satisfied = False
    if tp.pattern == 'Selfloop':
        satisfied = satisfy_Selfloop(tp.event1, trace)
    # elif tp.pattern == 'Selfloop_e2':
    #     satisfied = satisfy_Selfloop(tp.event2, trace)
    elif tp.pattern == 'Alternating':
        satisfied = satisfy_Alternating(tp, trace)
    elif tp.pattern == 'Eventually':
        satisfied = satisfy_Alternating(tp, trace)
    return satisfied

def satisfy_Selfloop(event, trace):
    listOfEventIndexes = []
    for i in range(len(trace)):
        if trace[i] == event:
            # print(i)
            listOfEventIndexes.append(i)
    # print(f'listOfEventIndexes:{listOfEventIndexes}')

    count = 1
    for i in range(len(listOfEventIndexes) - 1):
        current_item = listOfEventIndexes[i]
        next_item = listOfEventIndexes[i + 1]

        if next_item == current_item+1:
            count+=1
    if count > 1:
        return True
    else:
        return False

def satisfy_Alternating(tp, trace):
    event1 = tp.event1
    event2 = tp.event2
    satisfied = False
    listOfEvent1Indexes = []
    for i in range(len(trace)-1):
        if trace[i] == event1 and trace[i+1]==event2:
            listOfEvent1Indexes.append(i)

    count = 1
    for i in range(len(listOfEvent1Indexes) - 1):
        current_item = listOfEvent1Indexes[i]
        next_item = listOfEvent1Indexes[i + 1]

        if next_item == current_item + 2:
            count += 1
    if count > 1:
        return True
    else:
        return False

def satisfy_Eventually(event1, event2, trace):
    satisfied = False
    current_i = 0
    event1_found = False
    for i in range(current_i, len(trace)):
        if trace[i] == event1:
            event1_found = True
            current_i = i+1
            break
    for i in range(current_i, len(trace)):
        if trace[i] == event2 and event1_found:
            satisfied = True

    return satisfied



if __name__ == '__main__':
    traces = [['L0', 'L1', 'L1', 'L0','L1', 'L2'],
              ['L0', 'L0', 'L2', 'L2', 'L0', 'L2',   'L1', 'L2'],
              ['L0', 'L2', 'L1', 'L1', 'L1'],
              ['L3', 'L1','L0', 'L1', 'L0', 'L1'],
              ['L0', 'L0', 'L0', 'L2', 'L2', 'L2'],
              ['L1', 'L1', 'L2', 'L0', 'L0'],
              ['L0', 'L1', 'L0', 'L0', 'L1', 'L1', 'L2']]
    event1 = 'L0'
    event2 = 'L1'
    for trace in traces:
        print(f'Trace: {trace}')
        print(f'satisfied Alternating pattern for event \' {event1}\' and event\'{event2}\'?'
              f' {satisfy_Eventually(event1, event2, trace)}')