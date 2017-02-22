#!/usr/bin/python
import smbus
from time import sleep

bus = smbus.SMBus(1)

# ADXL345 constants
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004

DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D

MEASURE             = 0x08
AXES_DATA           = 0x32

class Accelerometer:

    address = None

    def __init__(self, address=0x53):
        self.address = address
        self.enable_measurement()

    def enable_measurement(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)

    def get_acceleration_raw(self):
        ''' Returns raw readings from the sensor'''
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)

        x = bytes[0] | (bytes[1] << 8)
        if x & (1 << 16 - 1):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if y & (1 << 16 - 1):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if z & (1 << 16 - 1):
            z = z - (1<<16)

        return (x, y, z)

    def get_acceleration(self, gforce=False):
        '''
        returns the current reading of acceleration from the sensort as a vector

        parameter gforce:
        False (default): result is returned in m/s^2
        True           : result is returned in gs
        '''
        (x, y, z) = self.get_acceleration_raw()

        x = x * SCALE_MULTIPLIER
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if  gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        return (x, y, z)
