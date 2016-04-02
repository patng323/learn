
from mrjob.job import MRJob, MRStep
import mrjob
import csv
import sys

def csv_readline(line):
    return csv.reader([line]).next()

class testSecSort(MRJob):
    INTERNAL_PROTOCOL = mrjob.protocol.RawProtocol
    OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
    
    def mapper1(self, line_no, line):
        cell = csv_readline(line)
        yield cell[0], "\t".join(cell[1:])

    def reducer1(self, key, value):
        print type(value)
        yield key, ",".join(["["+str(v)+"]" for v in value])

    def steps(self):
        return [
            MRStep(mapper=self.mapper1,
                   reducer=self.reducer1,
                    jobconf={
                    "stream.num.map.output.key.fields":"3",
                    "mapred.output.key.comparator.class":
                        "org.apache.hadoop.mapred.lib.KeyFieldBasedComparator",
                    "mapred.text.key.comparator.options":"-k1,1n -k3,3nr",
                          })]
    
if __name__ == '__main__':
    testSecSort.run()