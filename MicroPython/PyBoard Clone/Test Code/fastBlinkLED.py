# fastBlinkLED.py -- put your code here!

import time
import pyb

def fastBlinkLED():
	while True:
		pyb.LED(1).on()
		pyb.LED(1).off()

fastBlinkLED()
