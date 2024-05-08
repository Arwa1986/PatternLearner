import random
from PattrenFromTraces.TemporalPeoperty import TemporalProperty

properties = []

def discover_patterns_fromTraces(Positive_traces, alphabet):
    for char in alphabet:
        calculate_satisfactory(char, '', Positive_traces, 'Selfloop')
    events_pairs = get_events_pairs(alphabet)
    print(f'Events Pairs: {events_pairs}')
    for pair in events_pairs:
        event1 = pair[0]
        event2 = pair[1]
        patterns = ['Alternating', 'Eventually']
        for patrn in patterns:
            calculate_satisfactory(event1, event2, Positive_traces, patrn)
            # calculate_satisfactory(event2, event1, Positive_traces, patrn)

    properties.sort(key=lambda x: x.get_weigth(), reverse=True)

    for tp in properties:
        tp.print()
    avgWeigth = get_average_weigth()
    return properties , avgWeigth
def get_events_pairs(alphabet):
    events_pairs=[]
    for i in  range(len(alphabet)-1):
        for j in range(i+1, len(alphabet)):
            event1 = alphabet[i]
            event2 = alphabet[j]
            events_pairs.append([event1, event2])
    return events_pairs

def pick_random_events(alphabet):
    # Pick a random state from the list
    e1 = random.choice(alphabet)
    alphabet.remove(e1)
    e2 = random.choice(alphabet)
    alphabet.remove(e2)
    return e1, e2

def calculate_satisfactory(event1, event2, traces, patrn):
    tp = TemporalProperty(event1,event2, patrn)
    for trace in traces:
        frequent_occurr = calculate_frequent_occurrence(tp, trace)
        if  frequent_occurr> 0:
            tp.counter+= frequent_occurr
    properties.append(tp)
    # print(f'Total frequent occurrence: {tp.counter}')

def calculate_frequent_occurrence(tp, trace):
    frequent_occurrence = 0
    if tp.pattern == 'Selfloop':
        frequent_occurrence = satisfy_Selfloop(tp.event1, trace)
    elif tp.pattern == 'Alternating':
        frequent_occurrence = satisfy_Alternating(tp.event1, tp.event2, trace)
    elif tp.pattern == 'Eventually':
        frequent_occurrence = satisfy_Eventually(tp.event1, tp.event2, trace)

    return frequent_occurrence

def satisfy_Selfloop(event, trace):
    # return the number of Alternating patterns occurs in one trace
    # an event must be repeated two or more times to consider an occurrence of pattern
    # return 0 if pattern is not satisfied by the trace
    i=0
    count = 0
    pattern_counter = 0
    while i< len(trace):
        while i < len(trace) and trace[i] == event:
            count += 1
            i += 1
        if count > 1:
            pattern_counter += 1
        count = 0
        i+=1
    return pattern_counter

def satisfy_Alternating(event1, event2, trace):
    # return the number of Alternating patterns occurs in one trace
    # event1 followed by one or more occurrence of event2
    # return 0 if pattern is not satisfied by the trace
    count = 0
    for i in range(len(trace)-1):
        if trace[i] == event1 and trace[i+1]==event2:
            i +=1
            count+=1
    return count

def satisfy_Eventually(event1, event2, trace):
    # return the number of Eventually patterns occurs in one trace
    # eventually means event1 occurs 1:many times followed by one or more occurrence of event2
    # return 0 if pattern is not satisfied by the trace
    current_i = 0
    event1_counter = 0
    counter = 0
    while current_i < len(trace):
        while  current_i<len(trace) and trace[current_i] == event1:
                event1_counter += 1
                current_i +=1

        if current_i<len(trace) and trace[current_i] == event2 and event1_counter>1:
                counter+=1

        current_i += 1
        event1_counter = 0

    return counter

def get_average_weigth():
    average_weight = 0
    total_weigth = 0
    for p in properties:
        total_weigth += p.get_weigth()
    average_weight = total_weigth/len(properties)
    return average_weight
if __name__ == '__main__':
    traces = [['L0', 'L1', 'L1', 'L0','L1', 'L2'],
              ['L0', 'L0', 'L2', 'L2', 'L0', 'L0', 'L1', 'L2'],
              ['L0', 'L1', 'L1', 'L1', 'L1'],
              ['L3', 'L1','L0', 'L1', 'L0', 'L1'],
              ['L0', 'L0', 'L0', 'L2', 'L2', 'L2'],
              ['L1', 'L1', 'L2', 'L0', 'L0'],
              ['L1', 'L0', 'L0', 'L0', 'L1', 'L1', 'L2']]
    # event1 = 'L0'
    # event2 = 'L1'
    # print(f'selfloop pattern\n event1: \' {event1}\'')# and event2:\'{event2}\'')
    # for trace in traces:
    #     print(f'Trace: {trace}')
    #     print(f'pattern found {satisfy_Selfloop(event1, trace)} times')
    discover_patterns_fromTraces(traces, ['L0', 'L1'])


# selfloop pattern
#  event1: ' L0'
# Trace: ['L0', 'L1', 'L1', 'L0', 'L1', 'L2']
# pattern found 0 times
# Trace: ['L0', 'L0', 'L2', 'L2', 'L0', 'L0', 'L1', 'L2']
# pattern found 2 times
# Trace: ['L0', 'L1', 'L1', 'L1', 'L1']
# pattern found 0 times
# Trace: ['L3', 'L1', 'L0', 'L1', 'L0', 'L1']
# pattern found 0 times
# Trace: ['L0', 'L0', 'L0', 'L2', 'L2', 'L2']
# pattern found 1 times
# Trace: ['L1', 'L1', 'L2', 'L0', 'L0']
# pattern found 1 times
# Trace: ['L1', 'L0', 'L0', 'L0', 'L1', 'L1', 'L2']
# pattern found 1 times

# Alternating pattern
#  event1: ' L0' and event2:'L1'
# Trace: ['L0', 'L1', 'L1', 'L0', 'L1', 'L2']
# pattern found 2 times
# Trace: ['L0', 'L0', 'L2', 'L2', 'L0', 'L0', 'L1', 'L2']
# pattern found 1 times
# Trace: ['L0', 'L1', 'L1', 'L1', 'L1']
# pattern found 1 times
# Trace: ['L3', 'L1', 'L0', 'L1', 'L0', 'L1']
# pattern found 2 times
# Trace: ['L0', 'L0', 'L0', 'L2', 'L2', 'L2']
# pattern found 0 times
# Trace: ['L1', 'L1', 'L2', 'L0', 'L0']
# pattern found 0 times
# Trace: ['L1', 'L0', 'L0', 'L0', 'L1', 'L1', 'L2']
# pattern found 1 times

# Eventually pattern
#  event1: ' L0' and event2:'L1'
# Trace: ['L0', 'L1', 'L1', 'L0', 'L1', 'L2']
# pattern found 2 times
# Trace: ['L0', 'L0', 'L2', 'L2', 'L0', 'L0', 'L1', 'L2']
# pattern found 1 times
# Trace: ['L0', 'L1', 'L1', 'L1', 'L1']
# pattern found 1 times
# Trace: ['L3', 'L1', 'L0', 'L1', 'L0', 'L1']
# pattern found 2 times
# Trace: ['L0', 'L0', 'L0', 'L2', 'L2', 'L2']
# pattern found 0 times
# Trace: ['L1', 'L1', 'L2', 'L0', 'L0']
# pattern found 0 times
# Trace: ['L1', 'L0', 'L0', 'L0', 'L1', 'L1', 'L2']
# pattern found 1 times
