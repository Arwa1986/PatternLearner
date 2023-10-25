from SatPatterns_RandFSM import (run_)
from input_reader import import_input

if __name__ == '__main__':
    accepted, rejected= import_input('exp1.txt')
    run_(accepted, ['L0', 'L1'])