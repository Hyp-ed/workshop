#!/usr/bin/python
from vl6180 import Proximity
import thread
import time

def get_avg_dist_transaction(n, data_out, lock):
    lock.acquire()
    sum = 0
    for i in xrange(0, int(n)):
        sum += p.get_distance()
    data_out[0] = float(sum) / n
    lock.release()

p = Proximity()

def get_avg_dist(num_measurements):
    lock = thread.allocate_lock()
    data = [0]
    thread.start_new_thread(get_avg_dist_transaction, (num_measurements, data, lock))
    time.sleep(0.001)
    lock.acquire()
    result = data[0]
    lock.release()
    return result

# Initialize
print 'Measuring distance to wall...'
base_dist = get_avg_dist(50)
print 'Distance to wall is {0:.0f} mm'.format(base_dist)
n = 40
tolerance = 3.5
last_dist = base_dist

while True:
    d = get_avg_dist(n)
    if d < last_dist - tolerance:
        # New object
        width = base_dist - d
        print 'Object detected with width of {:.0f} mm'.format(width)
        last_dist = d
    if d > last_dist + tolerance:
        # New (narrower) object or no object
        if d > base_dist - tolerance:
            # No object present
            print 'Object removed'
            last_dist = base_dist
        else:
            # New object
            width = base_dist - d
            print 'Object detected with width of {:.0f} mm'.format(width)
            last_dist = d
