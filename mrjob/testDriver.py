from test import test
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-r", type=str, default='inline')
args = parser.parse_args()

mr_job = test(args=['test0.data', '-r', args.r, '--strict-protocols'])
with mr_job.make_runner() as runner: 
    runner.run()
    print "Secondary sort using the 3rd field in reverse order:"
    for line in runner.stream_output():
        print line
        