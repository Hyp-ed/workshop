#!/usr/bin/python

from time import time
from mpu6050 import read_accl_data, ACCL_SCALE

def get_offset():
    xsum = 0
    ysum = 0
    zsum = 0
    n = 2000.0
    for i in xrange(0,int(n)):
        (x,y,z) = read_accl_data()
        xsum += x
        ysum += y
        zsum += z - ACCL_SCALE
    return (xsum/n, ysum/n, zsum/n)

(x_off, y_off, z_off) = get_offset()

def get_scaled_data():
    (x,y,z) = read_accl_data()
    return ((x - x_off)/ACCL_SCALE, (y - y_off)/ACCL_SCALE, (z - z_off)/ACCL_SCALE)

n=0
tt=0
(vel_x, vel_y, vel_z) = (0.0, 0.0, 0.0)
t0 = time()
(x0, y0, z0) = get_scaled_data()
while True:
    (x, y, z) = get_scaled_data()
    t = time()
    dt = t-t0
    vel_x += (x + x0)*5 * dt
    vel_y += (y + y0)*5 * dt
    vel_z += (z + z0 - 2.0)*5 * dt
    t0 = t
    (x0, y0, z0) = (x, y, z)
    print 'x={0:12.6f}|     y={1:12.6f}|     z={2:12.6f}'.format(vel_x, vel_y, vel_z)