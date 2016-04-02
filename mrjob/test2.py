
from mrjob.job import MRJob, MRStep
import mrjob
import csv
import sys

class test2(MRJob):
    def configure_options(self):
        super(test2, self).configure_options()
        # Notice the dest attribute
        self.add_passthrough_option('--max-age', dest='maxAge', type='int', default=5)
        self.add_passthrough_option('--unitTest', action="store_true")
        
    def load_options(self, args):
        super(test2, self).load_options(args)
        # Not necessary unless you need to do something special here.
        
    def mapper(self, line_no, line):
        fields = line.split(',')
        v = ("apple","boy","cat", "dog")
        yield fields[0], (v, len(fields), self.options.maxAge, self.options.unitTest)

if __name__ == '__main__':
    test2.run()