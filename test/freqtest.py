#!/usr/bin/python

import smbus
import math
from time import time
import cPickle

from mpu6050 import *

t0 = time()
n = 10000
arr = [0]*n
print "reading..."
t1 = time()
for i in xrange(0,n):
    arr[i] = (read_accl_data(), read_gyro_data(), time())
t2 = time()

#for d in arr:
#    print d
    
print "Time to get ", n, " readings: ", t2-t1, " seconds"

t1 = time()
f = open('gyro_accel_time.list.pkl', 'wb')
cPickle.dump(arr, f, cPickle.HIGHEST_PROTOCOL)
f.close()
t2 = time()
    
print "Time to pickle: ", t2-t1, " seconds"
print (time() - t0)
