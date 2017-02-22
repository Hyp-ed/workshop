#!/usr/bin/python
import math
from mpu6050 import Accelerometer, Gyro
import threading
from time import time


class Rotation:
    def __init__(self):
        self._thread = RotationThread(0.75)
        self.start()

    def __del__(self):
        self.stop()

    def start(self):
        if not self._thread.stop or self._thread.is_alive():
            return # already started
        self._thread.start()

    def stop(self):
        self._thread.stop = True

    def get_rotation(self):
        r = self._thread.rotation
        # return a representation of rotation ccalculated from r
        return r


class RotationThread(threading.Thread):
    def __init__(self, gyro_weight):
        threading.Thread.__init__(self)
        self.rotation = (0.0, 0.0, 0.0)
        self.stop = True
        self._gw = gyro_weight     # gyro weight
        self._aw = 1 - gyro_weight # accl weight
        self._accl = Accelerometer()
        self._gyro = Gyro()
        self._gyro.stop_integration()

    def run(self):
        self.rotation = (0.0, 0.0, 0.0)
        self.stop = False
        t0 = time()
        omega0 = self._gyro.get_angular_velocity()
        while not self.stop:
            #print self.rotation
            accl = self._accl.get_acceleration()
            t = time()
            omega = self._gyro.get_angular_velocity()
            dt = t - t0
            dr_gyro = tuple((v0 + v)*dt/2 for (v0, v) in zip(omega0, omega))
            r = self.rotation
            r_gyro = tuple(a0 + da for (a0, da) in zip(r, dr_gyro))
            r_accl = (get_x_rotation(accl[1], accl[2]), get_y_rotation(accl[0], accl[2]), r_gyro[2]) # yaw cannot be calculated using accelerometer so use just the gyro value
            
            # Calculate the waighted average of accelerometer and gyro rotations
            
            r = tuple(a*self._aw + g*self._gw for (a, g) in zip(r_accl, r_gyro))
            self.rotation = r
            t0 = t
            omega0 = omega


def cross((a, b, c), (x, y, z)):
    return (b*z - c*y, c*x - a*z, a*y - b*x)


def norm((x, y, z)):
    return math.sqrt(x*x + y*y + z*z)


def get_x_rotation(y,z):
    '''Calculates roll'''
    radians = math.atan2(y, z)
    return math.degrees(radians)


def get_y_rotation(x,z):
    '''Calculates pitch'''
    radians = math.atan2(-x, z)
    return math.degrees(radians)