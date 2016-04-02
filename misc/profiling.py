import cProfile
import random
from collections import Counter

# Set the seed for repeatability.

random.seed(0)

# Create 1m dictionaries with 26 elements each for the test.

samples = [
	{ ch: random.randint(0, 10) for ch in 'abcdefghijklmnopqrstuvwxyz' }
		for i in range(0, 1000000)
]

"""
Combine dictionaries.
"""
def combine_dicts(samples):
	complete = {}

	for sample in samples:
		for key, value in sample.iteritems():
			if key in complete:
				complete[key] += value
			else:
				complete[key] = value

"""
Update counters.
"""
def update_counters(samples):
	counter = Counter()

	for sample in samples:
		counter.update(sample)

	return counter

# Perform the profiling test.

print 'combine_dicts():', cProfile.run('combine_dicts(samples)')
print 'update_counters():', cProfile.run('update_counters(samples)')
