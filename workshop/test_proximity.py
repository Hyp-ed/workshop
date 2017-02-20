#!/usr/bin/python
from vl6180 import Proximity

sensor = Proximity()
print sensor.get_distance()