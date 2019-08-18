###############################################################################
# blinkI2CIO8_pca9544 - I2CIO8 Blink Example
# Run with 
#	import blinkI2CIO8_pca9544
###############################################################################

import time
import machine
import test_pca9544

def blinkLED0():
	test_pca9544.pinMode(0,test_pca9544.OUTPUT)
	while True:
		test_pca9544.digitalWrite(0,1)
		time.sleep(0.25)
		test_pca9544.digitalWrite(0,0)
		time.sleep(0.25)

blinkLED0()
