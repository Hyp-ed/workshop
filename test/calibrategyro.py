#!/usr/bin/python

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write(addr, data):
    high = (data & 0xff00) >> 8
    low = (data & 0xff)
    bus.write_byte_data(address, addr, high)
    bus.write_byte_data(address, addr + 1, low)

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

def set_gyro_offset(x, y, z):
    write(0x13, x)
    write(0x15, y)
    write(0x17, z)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

#print 'Calibrating... (will take a minute or two)'
print 'Not working'
set_gyro_offset(0, 0, 0)
'''
xsum = 0
ysum = 0
zsum = 0
n = 1000
for i in xrange(0, n):
    (x,y,z) = read_gyro_data()
    xsum += x
    ysum += y
    zsum += z

ofst_x = xsum/n
ofst_y = ysum/n
ofst_z = zsum/n
set_gyro_offset(ofst_x, ofst_y, ofst_z)

print 'DONE! (offset: ', (ofst_x, ofst_y, ofst_z), ')'
print read_word_2c(0x13)
'''
