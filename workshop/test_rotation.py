#!/usr/bin/python
from rotation import Rotation

r = Rotation()

x = raw_input()
while x == '':
    print r.get_rotation()
    x = raw_input()
r.stop()