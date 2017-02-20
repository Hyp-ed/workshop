#!/usr/bin/python
from i2c import I2C

class Proximity:
    def __init__(self, address = 0x29):
        self._i2c = I2C(1, address, 16)
        self._initialize()

    def _initialize(self):
        setup = self._i2c.read_reg(0x016)
        if setup == 1:
            self._i2c.write_reg(0x0207, 0x01)
            self._i2c.write_reg(0x0208, 0x01)
            self._i2c.write_reg(0x0096, 0x00)
            self._i2c.write_reg(0x0097, 0xfd)
            self._i2c.write_reg(0x00e3, 0x00)
            self._i2c.write_reg(0x00e4, 0x04)
            self._i2c.write_reg(0x00e5, 0x02)
            self._i2c.write_reg(0x00e6, 0x01)
            self._i2c.write_reg(0x00e7, 0x03)
            self._i2c.write_reg(0x00f5, 0x02)
            self._i2c.write_reg(0x00d9, 0x05)
            self._i2c.write_reg(0x00db, 0xce)
            self._i2c.write_reg(0x00dc, 0x03)
            self._i2c.write_reg(0x00dd, 0xf8)
            self._i2c.write_reg(0x009f, 0x00)
            self._i2c.write_reg(0x00a3, 0x3c)
            self._i2c.write_reg(0x00b7, 0x00)
            self._i2c.write_reg(0x00bb, 0x3c)
            self._i2c.write_reg(0x00b2, 0x09)
            self._i2c.write_reg(0x00ca, 0x09)
            self._i2c.write_reg(0x0198, 0x01)
            self._i2c.write_reg(0x01b0, 0x17)
            self._i2c.write_reg(0x01ad, 0x00)
            self._i2c.write_reg(0x00ff, 0x05)
            self._i2c.write_reg(0x0100, 0x05)
            self._i2c.write_reg(0x0199, 0x05)
            self._i2c.write_reg(0x01a6, 0x1b)
            self._i2c.write_reg(0x01ac, 0x3e)
            self._i2c.write_reg(0x01a7, 0x1f)
            self._i2c.write_reg(0x0030, 0x00)

            # Recommended : Public registers - See data sheet for more detail
            
            self._i2c.write_reg(0x0011, 0x10) # Enables polling for 'New Sample ready' when measurement completes
            self._i2c.write_reg(0x010a, 0x30) # Set the averaging sample period (compromise between lower noise and increased execution time)
            self._i2c.write_reg(0x003f, 0x46) # Sets the light and dark gain (upper nibble). Dark gain should not be changed.
            self._i2c.write_reg(0x0031, 0xFF) # sets the # of range measurements after which auto calibration of system is performed
            self._i2c.write_reg(0x0040, 0x63) # Set ALS integration time to 100ms
            self._i2c.write_reg(0x002e, 0x01) # perform a single temperature calibratio of the ranging sensor
            self._i2c.write_reg(0x001b, 0x09) # Set default ranging inter-measurement period to 100ms
            self._i2c.write_reg(0x003e, 0x31) # Set default ALS inter-measurement period to 500ms
            self._i2c.write_reg(0x0014, 0x24) # Configures interrupt on 'New Sample Ready threshold event' 

            self._i2c.write_reg(0x016, 0x00)
    
    def start_range(self):
        self._i2c.write_reg(0x018, 0x01)

    def poll_range(self):
        # check the status
        status = self._i2c.read_reg(0x04f)
        range_status = status & 0x07
        # wait for new measurement ready status
        while range_status != 0x04:
            status = self._i2c.read_reg(0x04f)
            range_status = status & 0x07

    def clear_interrupts(self):
        self._i2c.write_reg(0x015, 0x07)

    def get_distance(self):
        self.start_range()
        self.poll_range()
        rng = self._i2c.read_reg(0x062)
        self.clear_interrupts()
        return rng