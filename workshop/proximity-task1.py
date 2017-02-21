#!/usr/bin/python
from vl6180 import Proximity
import threading

p = Proximity()

def get_avg_dist(num_measurements):
    sum = 0
    for i in xrange(0, int(num_measurements)):
        sum += p.get_distance()
    return float(sum) / num_measurements

# Initialize
print 'Measuring distance to wall...'
base_dist = get_avg_dist(32)
print 'Distance to wall is {0:.3f} mm'.format(base_dist)
n = 8
tolerance = 2.5
last_dist = base_dist

while True:
    d = get_avg_dist(n)
    if d > last_width + tolerance:
        # New object
        width = d - base_dist
        print 'Object detected with width of {:.3f} mm'.format(width)
        last_dist = d
    if d < last_dist - tolerance:
        # New (narrower) object or no object
        if d < base_dist + tolerance:
            # No object present
            print 'Object removed'
            last_dist = base_dist
        else:
            # New object
            width = d - base_dist
            print 'Object detected with width of {:.3f} mm'.format(width)
            last_dist = d
