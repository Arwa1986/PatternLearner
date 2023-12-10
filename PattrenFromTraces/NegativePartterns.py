from random import random

from PattrenFromTraces.APTA import APTA
from PattrenFromTraces.PatternsChecker import has_selfloop, has_Alternating
from PattrenFromTraces.matrix_reader import *


def build_adjs_matrix(input_file):
    # open original file
    input = [l.strip().lower() for l in open(input_file).readlines()]

    # create file named "matrixOfRefrencedAuotmata.adjlist"
    # W: will overwirte any previous contents
    f = open("input\matrixOfRefrencedAuotmata.adjlist", "w")

    for line in input:
        if not line or line.strip().startswith("#") or line.strip() == '':
            continue
        elif line in ['postive sequences', 'positive sequences', 'negative sequences']:
            break

        list = [l.strip().upper() for l in line.replace(' - ',',').replace(' -> ',',').split(',') if l != ""]
        row = list[0].split('<', 1)[0] + ' ' +list[2].split('<', 1)[0] + ' ' + list[1] +'\n'
        f.write(row)

    f.close()

def pick_random_events(alphabet):
    # Pick a random state from the list
    e1 = random.choice(alphabet)
    alphabet.remove(e1)
    e2 = random.choice(alphabet)
    alphabet.remove(e2)
    return e1, e2

if __name__ == '__main__':
    # build the refrence graph
    # from txt file to adj matrex
    build_adjs_matrix('input\PosNegExamples.txt')
    #from adj matrixx to graph
    G, alphabet = read_matrix('input\matrixOfRefrencedAuotmata.adjlist')
    print(f'Alphabet: {alphabet}')
    draw(G, "output/RefrencedAuotmata.png")

    # built APTA object to use functions
    apta_obj = APTA()
    apta_obj.G = G
    apta_obj.alphabet = alphabet
    apta_obj.root = 'V0'

    # check negative patterns
    negative_selfloop = []
    for char in alphabet:
        if not has_selfloop(apta_obj, char):
            negative_selfloop.append(char)

    print(f'Negative selfloop: {negative_selfloop}')

    negative_alternating=[]


    while alphabet:
         event1, event2 = pick_random_events(alphabet)
         if not has_Alternating(event2, event1):# rewrite method to search in graph not in trace
             break