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
        return (norm(r), r)


class RotationThread(threading.Thread):
    def __init__(self, gyro_weight):
        threading.Thread.__init__(self)
        self.rotation = (0.0, 0.0, 0.0)
        self.stop = True
        self._gw = gyro_weight
        self._aw = 1 - gyro_weight
        self._accl = Accelerometer()
        self._gyro = Gyro()
        self._gyro.stop_integration()

    def run(self):
        self.rotation = (0.0, 0.0, 0.0)
        self.stop = False
        #accl0 = self._accl.get_acceleration_raw()
        t0 = time()
        omega0 = self._gyro.get_angular_velocity()
        while not self.stop:
            #print self.rotation
            accl = self._accl.get_acceleration_raw()
            t = time()
            omega = self._gyro.get_angular_velocity()
            dt = t - t0
            dr_gyro = tuple((v0 + v)*dt/2 for (v0, v) in zip(omega0, omega))
            n = norm(accl)
            angle = math.degrees(math.acos(accl[2] / n))
            axis = (accl[1]/n, -accl[0]/n, 0)
            r = self.rotation
            dr_accl = (angle*axis[0] - r[0], angle*axis[1] - r[1], dr_gyro[2])
            dr = tuple(a*self._aw + g*self._gw for (a, g) in zip(dr_accl, dr_gyro))
            r = tuple(a+b for (a, b) in zip(r, dr))
            self.rotation = r
            t0 = t
            omega0 = omega


def cross((a, b, c), (x, y, z)):
    return (b*z - c*y, c*x - a*z, a*y - b*x)


def norm((x, y, z)):
    return math.sqrt(x*x + y*y + z*z)