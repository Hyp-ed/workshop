#!/usr/bin/python
from mpu6050 import Gyro

gyro = Gyro()

x = raw_input()
while x == '':
    print gyro.get_angular_position()
    x = raw_input()
gyro.stop_integration()