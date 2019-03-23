# readAccelLoop.py
# Read the on-board accellerator and sent to the serial port

import pyb

accel = pyb.Accel()
light = pyb.LED(3)
SENSITIVITY = 3

while True:
	print(accel.x(),accel.y(),accel.z())
	