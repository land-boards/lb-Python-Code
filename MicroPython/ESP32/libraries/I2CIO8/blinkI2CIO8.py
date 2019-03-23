###############################################################################
# blinkI2CIO8 - I2CIO8 Blink Example
###############################################################################

import time
import machine
import I2CIO8

def blinkLED0():
	I2CIO8.pinMode(0,I2CIO8.OUTPUT)
	while True:
		I2CIO8.digitalWrite(0,1)
		time.sleep(0.25)
		I2CIO8.digitalWrite(0,0)
		time.sleep(0.25)
