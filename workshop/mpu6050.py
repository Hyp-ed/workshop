#!/usr/bin/python
from i2c import I2C
import threading
from time import time

DEFAULT_ADDRESS = 0x68
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_short_signed(i2c, addr):
    high = i2c.read_reg(addr)
    low = i2c.read_reg(addr + 1)
    val = (high << 8) | low # unsigned
    if val >= 0x8000:
        return -((0xffff - val) + 1)
    else:
        return val


class Accelerometer:
    def __init__(self, address = DEFAULT_ADDRESS):
        self._i2c = I2C(1, address, 8)
        self._i2c.write_reg(power_mgmt_1, 0)
        self.SCALE = 16384.0

    def get_acceleration_raw(self):
        x = read_short_signed(self._i2c, 0x3b)
        y = read_short_signed(self._i2c, 0x3d)
        z = read_short_signed(self._i2c, 0x3f)
        return (x, y, z)

    def get_acceleration(self):
        (x, y, z) = self.get_acceleration_raw()
        return (x / self.SCALE, y / self.SCALE, z / self.SCALE)


class Gyro:
    def __init__(self, address = DEFAULT_ADDRESS):
        self._i2c = I2C(1, address, 8)
        self._i2c.write_reg(power_mgmt_1, 0)
        self.SCALE = 131.0
        self._position_thread = GyroThread(self)
        self._calibrate()
        self.start_integration()

    def __del__(self):
        self.stop_integration()

    def _calibrate(self):
        tot = (0, 0, 0)
        n = 1000.0
        print 'Calibrating gyro...'
        for i in xrange(0, int(n)):
            v = self.get_angular_velocity_raw()
            tot = tuple(s + x for (s,x) in zip(tot, v))
        print 'Gyro calibrated'
        self._offset = tuple(-x/n for x in tot)

    def start_integration(self):
        if not self._position_thread.stop or self._position_thread.is_alive():
            return # already started
        self._position_thread.stop = False
        self._position_thread.start()

    def stop_integration(self):
        self._position_thread.stop = True

    def get_angular_velocity_raw(self):
        x = read_short_signed(self._i2c, 0x43)
        y = read_short_signed(self._i2c, 0x45)
        z = read_short_signed(self._i2c, 0x47)
        return (x, y, z)

    def get_angular_velocity(self):
        v = self.get_angular_velocity_raw()
        return tuple((a + b)/self.SCALE for (a, b) in zip(v, self._offset))

    def get_angular_position(self):
        return self._position_thread.pos

    def update_pos(self, pos):
        self._position_thread.pos = pos


class GyroThread(threading.Thread):
    def __init__(self, gyro):
        threading.Thread.__init__(self)
        self._gyro = gyro
        self.stop = True
        self.pos = (0.0, 0.0, 0.0)

    # ========== EXERCISE 1 STARTS HERE ========================================
    # The sensor only measures the angular velocity. In order to get the angular
    # displacement (the angles through which the sensor has rotated about each
    # of the axes) we need to mutiply the velocity by time. Since the velocity
    # is not constant over time, we need to take readings as often as possible
    # and assume that the velocity doesn't change too much during the very tiny
    # time intervals between readings.
    # Your task will be to understand the code below that does that and perform
    # the key calculation.
    def run(self):
        self.pos = (0.0, 0.0, 0.0) # this will hold the total angles the sensor has rotated through
        self.stop = False # not important
        t0 = time() # time of the first measurement
        v0 = self._gyro.get_angular_velocity() # first measurement
        while not self.stop:
            t = time() # time of the next measurement
            v = self._gyro.get_angular_velocity() # next measurement
            dt = t - t0 # calculate the time difference between the two measurements
            (x_v0, y_v0, z_v0) = v0 # split the first velocity measurement into the x, y and z components
            (x_v, y_v, z_v) = v # split the second velocity measurement into the x, y and z components
            (x_angle, y_angle, z_angle) = self.pos # split the total angles

            # Complete the following 3 lines calculating new values of the total angles
            x_angle = x_angle + (x_v0 + x_v)*dt/2
            y_angle = y_angle + (y_v0 + y_v)*dt/2
            z_angle = z_angle + (z_v0 + z_v)*dt/2

            self.pos = (x_angle, y_angle, z_angle)
            t0 = t # save the time of the last measurement to a variable that lives outside the loop
            v0 = v # save the measurement alongside the it was taken
