###############################################################################
# digio128 - DIGIO-128 library
###############################################################################

import time
import machine
import digio128

def blinkLED0():
	digio128.pinMode(0,digio128.OUTPUT)
	for loopCount in range(0,6):
		digio128.digitalWrite(0,1)
		time.sleep(0.25)
		digio128.digitalWrite(0,0)
		time.sleep(0.25)

blinkLED0()
