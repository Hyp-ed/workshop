from vl6180 import Sensor

s = Sensor()
#s._set_reg8(0x016, 0x01)
#print s._get_reg8(0x016)
print s.identify()
print s.range()
