#!/usr/bin/python

from time import time
import mpu6050
import math

def get_offset():
    xsum = 0
    ysum = 0
    zsum = 0
    n = 1000.0
    print "Calibrating gyro..."
    t = time()
    for i in xrange(0, int(n)):
        (x,y,z) = mpu6050.read_gyro_data()
        xsum += x
        ysum += y
        zsum += z
    return (xsum/n, ysum/n, zsum/n)
    t = time() - t
    print "Calibrated gyro on {} readings in {} seconds.".format(int(n), t)

(x_off, y_off, z_off) = get_offset()

def get_gyro_scaled():
    (x,y,z) = mpu6050.read_gyro_data()
    return ((x - x_off)/mpu6050.GYRO_SCALE, (y - y_off)/mpu6050.GYRO_SCALE, (z - z_off)/mpu6050.GYRO_SCALE)

def get_x_rotation(y, z):
    radians = math.atan2(y, z)
    return math.degrees(radians)

def get_y_rotation(x, z):
    radians = math.atan2(-x, z)
    return math.degrees(radians)

(gyro_x, gyro_y, gyro_z) = (0.0, 0.0, 0.0)
t0 = time()
r0 = get_gyro_scaled()
while True:
    (x, y, z) = mpu6050.read_accl_data()
    accl_x = get_x_rotation(y, z)
    accl_y = get_y_rotation(x, z)

    t = time()
    r = get_gyro_scaled()
    dt = t - t0
    gyro_x += (r0[0] + r[0]) / 2 * dt
    gyro_y += (r0[1] + r[1]) / 2 * dt
    gyro_z += (r0[2] + r[2]) / 2 * dt
    t0 = t
    r0 = r

    print 'gyro: x={0:12.6f}|     y={1:12.6f}|     z={2:12.6f}'.format(gyro_x, gyro_y, gyro_z)
    print 'accl: x={0:12.6f}|     y={1:12.6f}|'.format(accl_x, accl_y)