import itertools
import os
def transpoint():
    with open('transitionpoints.txt') as f:
        corpus=[i[32:] if(i[32].isdigit()) else i[33:] if(i[33].isdigit()) else i[34:] for i in list(itertools.islice(f, 0, None, 2))]
    return corpus
