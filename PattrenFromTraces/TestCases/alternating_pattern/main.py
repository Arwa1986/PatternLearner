from PattrenFromTraces.SatPatterns_RandFSM import satisfy_Alternating

if __name__ == '__main__':
    traces = [['L0', 'L1', 'L1', 'L0','L1', 'L2'],
              ['L0', 'L1', 'L2'],
              ['L0', 'L2', 'L1', 'L1', 'L1'],
              ['L3', 'L1','L0', 'L1', 'L0', 'L1'],
              ['L0', 'L1', 'L0', 'L1', 'L1', 'L2'],
              ['L0', 'L1', 'L2', 'L0', 'L1', 'L0', 'L1', 'L1', 'L2'],
              ['L0', 'L1', 'L0', 'L0', 'L1', 'L1', 'L2']]
    event1 = 'L0'
    event2 = 'L1'
    for trace in traces:
        print(f'Trace: {trace}')
        print(f'satisfied Alternating pattern for event \' {event1}\' and event\'{event2}\'?'
              f' {satisfy_Alternating(event1, event2, trace)}')

# Trace: ['L0', 'L1', 'L1', 'L0', 'L1', 'L2']
# satisfied Alternating pattern for event ' L0' and event'L1'? False
# Trace: ['L0', 'L1', 'L2']
# satisfied Alternating pattern for event ' L0' and event'L1'? False
# Trace: ['L0', 'L2', 'L1', 'L1', 'L1']
# satisfied Alternating pattern for event ' L0' and event'L1'? False
# Trace: ['L3', 'L1', 'L0', 'L1', 'L0', 'L1']
# satisfied Alternating pattern for event ' L0' and event'L1'? True
# Trace: ['L0', 'L1', 'L0', 'L1', 'L1', 'L2']
# satisfied Alternating pattern for event ' L0' and event'L1'? True
# Trace: ['L0', 'L1', 'L2', 'L0', 'L1', 'L0', 'L1', 'L1', 'L2']
# satisfied Alternating pattern for event ' L0' and event'L1'? True
# Trace: ['L0', 'L1', 'L0', 'L0', 'L1', 'L1', 'L2']
# satisfied Alternating pattern for event ' L0' and event'L1'? False
