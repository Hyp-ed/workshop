#!/usr/bin/python
import math
from adxl345 import Accelerometer

accl = Accelerometer()

print "accelerometer data"
print "------------------"

(accel_xout, accel_yout, accel_zout) = accl.get_acceleration_raw()

(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) = accl.get_acceleration()

print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled