#!/usr/bin/python

import io
import fcntl

IOCTL_I2C_SLAVE = 0x0703

class I2C:
    def __init__(self, bus_num, device_addr, addr_bits = 8):
        self._handle = io.open("/dev/i2c-" + str(bus_num), "r+b", buffering=0)
        fcntl.ioctl(self._handle, IOCTL_I2C_SLAVE, device_addr)
        self._addr_bits = addr_bits
    
    def __del__(self):
        if not self._handle.closed:
            self._handle.close()

    def read_reg(self, addr):
        """Read an 8-bit register at the address 'addr'"""
        dat = bytearray(self._addr_bits / 8)
        if self._addr_bits == 8:
            dat[0] = addr & 0xff
        if self._addr_bits == 16:
            dat[0] = (addr & 0xff00) >> 8 # MSB of register address
            dat[1] = addr & 0xff # LSB of register address
        self._handle.write(dat)
        return ord(self._handle.read(1))

    def write_reg(self, addr, data):
        dat = bytearray(self._addr_bits/8 + 1)
        if self._addr_bits == 8:
            dat[0] = addr & 0xff
            dat[1] = data & 0xff
        if self._addr_bits == 16:
            dat[0] = (addr & 0xff00) >> 8 # MSB of register address
            dat[1] = addr & 0xff # LSB of register address
            dat[2] = data & 0xff
        self._handle.write(dat)
