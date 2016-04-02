
from mrjob.job import MRJob, MRStep
import mrjob
import csv

import sys
def toStringKey(n):
    n = int(n)
    digits = len(str(sys.maxint))
    minInt = -sys.maxint - 1

    if n < 0:
        key = "-" + str(abs(minInt-n)).zfill(digits)
    else:
        key = str(n).zfill(digits)
        
    return key
    
class test(MRJob):
    SORT_VALUES = True
    
    def mapper(self, line_no, line):
        cell = line.strip().split(',')
        
        # Secondary sort using the 3rd field in reverse order
        yield cell[0], [toStringKey(sys.maxint - int(cell[2]))] + cell[1:]

    def reducer(self, key, value):
        yield key, [v[1:] for v in value]
        
if __name__ == '__main__':
    test.run()