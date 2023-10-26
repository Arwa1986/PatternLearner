from PattrenFromTraces.SatPatterns_RandFSM import satisfied_Selfloop

if __name__ == '__main__':
    traces = [['L0', 'L1', 'L1', 'L1', 'L2'], ['L0', 'L1', 'L2'], ['L0', 'L2', 'L1', 'L1', 'L1'], ['L0', 'L2', 'L1', 'L3', 'L1', 'L0', 'L1']]
    event = 'L1'
    for trace in traces:
        print(f'Trace: {trace}')
        print(f'satisfied selfloop pattern for event \' {event}\'? {satisfied_Selfloop(event, trace)}')


# expected result:
# Trace: ['L0', 'L1', 'L1', 'L1', 'L2']
# listOfEventIndexes:[1, 2, 3]
# satisfied selfloop pattern for event ' L1'? True
# Trace: ['L0', 'L1', 'L2']
# listOfEventIndexes:[1]
# satisfied selfloop pattern for event ' L1'? False
# Trace: ['L0', 'L2', 'L1', 'L1', 'L1']
# listOfEventIndexes:[2, 3, 4]
# satisfied selfloop pattern for event ' L1'? True
# Trace: ['L0', 'L2', 'L1', 'L3', 'L1', 'L0', 'L1']
# listOfEventIndexes:[2, 4, 6]
# satisfied selfloop pattern for event ' L1'? False
# Trace: ['L0', 'L1', 'L0', 'L1', 'L1', 'L2']
# listOfEventIndexes:[1, 3, 4]
# satisfied selfloop pattern for event ' L1'? True

