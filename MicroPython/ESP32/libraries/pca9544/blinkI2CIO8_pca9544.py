###############################################################################
# blinkI2CIO8_pca9544 - I2CIO8 Blink Example
###############################################################################

import time
import machine
import test_pca9544

def blinkLED0():
	pca9544.setI2CMuxPort(0)
	I2CIO8.pinMode(0,I2CIO8.OUTPUT)
	while True:
		I2CIO8.digitalWrite(0,1)
		time.sleep(0.25)
		I2CIO8.digitalWrite(0,0)
		time.sleep(0.25)

blinkLED0()
