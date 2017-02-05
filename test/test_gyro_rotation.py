#!/usr/bin/python

from time import time
from mpu6050 import read_gyro_data

def get_offset():
    xsum = 0
    ysum = 0
    zsum = 0
    n = 2000.0
    for i in xrange(0,int(n)):
        (x,y,z) = read_gyro_data()
        xsum += x
        ysum += y
        zsum += z
    return (xsum/n, ysum/n, zsum/n)

(x_off, y_off, z_off) = get_offset()

def get_scaled_data():
    scl = 131.0
    (x,y,z) = read_gyro_data()
    return ((x - x_off)/scl, (y - y_off)/scl, (z - z_off)/scl)

n=0
tt=0
(gyro_x, gyro_y, gyro_z) = (0.0, 0.0, 0.0)
t0 = time()
(x0, y0, z0) = get_scaled_data()
while True:
    (x, y, z) = get_scaled_data()
    t = time()
    dt = t-t0
    gyro_x += (x + x0)/2 * dt
    gyro_y += (y + y0)/2 * dt
    gyro_z += (z + z0)/2 * dt
    t0 = t
    (x0, y0, z0) = (x, y, z)
    print 'x={0:12.6f}|     y={1:12.6f}|     z={2:12.6f}'.format(gyro_x, gyro_y, gyro_z)
    
