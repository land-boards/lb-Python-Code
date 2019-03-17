###############################################################################
# testI2CIO8 - I2CIO8 Blink Example
###############################################################################

import time
import machine
import I2CIO8

def testI2CIO8():
	for port in range(0,4):
		I2CIO8.pinMode(port,I2CIO8.OUTPUT)
	while True:
		for port in range(0,4):
			I2CIO8.digitalWrite(port,1)
			time.sleep(0.5)
			I2CIO8.digitalWrite(port,0)
