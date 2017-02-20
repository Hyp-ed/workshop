#!/usr/bin/python

import smbus
import math

from mpu6050 import *

def get_rotation(x,y,z):
    angle = math.acos(z/math.sqrt(x*x + y*y + z*z))
    angle = math.degrees(angle)
    fac = math.sqrt(x*x + y*y)
    u = (y, -x, 0)
    return (angle, u)

def sgn(x):
    return math.copysign(1.0, x)

def get_y_rotation(x,z):
    radians = math.atan2(-x, z)
    return math.degrees(radians)
    #scl = math.sqrt(x*x + z*z)
    #x = x/scl
    #z = z/scl
    #return -90*sgn(x)+sgn(z)*sgn(x)*(90-abs(math.degrees(math.asin(x))))

def get_x_rotation(y,z):
    radians = math.atan2(y, z)
    return math.degrees(radians)
    #scl = math.sqrt(y*y + z*z)
    #y = y/scl
    #z = z/scl
    #return 90*sgn(y)-sgn(z)*sgn(y)*(90-abs(math.degrees(math.asin(y))))

print "gyro data"
print "---------"

(gyro_xout, gyro_yout, gyro_zout) = read_gyro_data()

print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131.0)
print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131.0)
print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131.0)

print
print "accelerometer data"
print "------------------"

(accel_xout, accel_yout, accel_zout) = read_accl_data()

scl = 16384.0
accel_xout_scaled = accel_xout / scl#/ 16384.0
accel_yout_scaled = accel_yout / scl#/ 16384.0
accel_zout_scaled = accel_zout / scl#/ 16384.0

print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

print "x rotation: " , get_x_rotation(accel_yout, accel_zout)
print "y rotation: " , get_y_rotation(accel_xout, accel_zout)
print "rotation: ", get_rotation(accel_xout, accel_yout, accel_zout)
print

print "temperature data"
print "----------------"
temp_out = read_temperature()
print "temp_out:", temp_out, " scaled: ", (temp_out + 521)/340.0
