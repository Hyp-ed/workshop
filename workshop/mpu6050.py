#!/usr/bin/python
from i2c import I2C

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

    def get_angular_velocity_raw(self):
        x = read_short_signed(self._i2c, 0x43)
        y = read_short_signed(self._i2c, 0x45)
        z = read_short_signed(self._i2c, 0x47)
        return (x, y, z)

    def get_angular_velocity(self):
        (x, y, z) = self.get_angular_velocity_raw()
        return (x / self.SCALE, y / self.SCALE, z / self.SCALE)
