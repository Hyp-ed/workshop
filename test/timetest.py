#!/usr/bin/python

import time

raw_input('start')
t=time.time()
c=time.clock()
raw_input('stop')
t=time.time()-t
c=time.clock()-c

print t
print c
