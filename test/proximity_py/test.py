#!/usr/bin/python

import vl6180

vl6180.initialize()
dist = vl6180.get_distance()
print dist
vl6180.close()