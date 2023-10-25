import random
from TemporalPeoperty import TemporalProperty
import re

properties = []

def run_(Positive_trace, alphabet):
    while alphabet:
        event1, event2 = pick_random_events(alphabet)
        calculate_satisfactory(event1, event2, Positive_trace)
        calculate_satisfactory(event2, event1, Positive_trace)

def pick_random_events(alphabet):
    # Pick a random state from the list
    e1 = random.choice(alphabet)
    alphabet.remove(e1)
    e2 = random.choice(alphabet)
    alphabet.remove(e2)
    return e1, e2

def calculate_satisfactory(event1, event2, traces):
    for trace in traces:
        tp = TemporalProperty(event1, event2)
        discover_pattren(tp, trace)
        if tp.strictest_pattern:
            # if at least one pattern is satisfied, store as a property
            properties.append(tp)
        print(f"trace: {trace}")
        tp.print()

def discover_pattren(tp, trace):
    cause = tp.event1
    effect = tp.event2
    # Define the regular expression pattern
    OneEffectPattern = f'[^{cause}]*({cause}[^{effect}]*{effect}[^{effect}{cause}]*)+'
    OneCausePattern = f'[^{cause}]*({cause}[^{effect}{cause}]*{effect}[^{cause}]*)+'
    CauseFirstPattern = f'[^{cause}{effect}]*({cause}[^{effect}]*{effect}[^{cause}]*)+'
    SelfLoop = f'{cause}+'

    if re.findall(OneEffectPattern, trace):
        tp.satisfy_1effect = True
    if re.findall(OneCausePattern, trace):
        tp.satisfy_1cause = True
    if re.findall(CauseFirstPattern, trace):
        tp.satisfy_causeFirst = True
    tp.discover_stricest_pattren()
