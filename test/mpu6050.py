#!/usr/bin/python

import smbus

GYRO_SCALE = 131.0
ACCL_SCALE = 16384.0

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


def read_byte(adr):
    return bus.read_byte_data(address, adr)


def read_word(adr):
    high = read_byte(adr)
    low = read_byte(adr+1)
    val = (high << 8) + low
    return val


def read_word_2c(adr):
    val = read_word(adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def read_gyro_data():
    x = read_word_2c(0x43)
    y = read_word_2c(0x45)
    z = read_word_2c(0x47)
    return (x, y, z)


def read_accl_data():
    x = read_word_2c(0x3b)
    y = read_word_2c(0x3d)
    z = read_word_2c(0x3f)
    return (x, y, z)


def read_temperature():
    t = read_word_2c(0x41)
    return t

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)
