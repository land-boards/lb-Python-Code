# blinkLED.py -- put your code here!

import time
import pyb

def blinkLED():
	pyb.LED(1).on()
	time.sleep(0.5)
	pyb.LED(1).off()

blinkLED()
