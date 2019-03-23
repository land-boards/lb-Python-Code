###############################################################################
# testI2CIO8 - I2CIO8 Blink Example
###############################################################################

import time
# import machine
import I2CIO8

def testI2CIO8():
	jumper0 = I2CIO8.digitalRead(4)
	jumper1 = I2CIO8.digitalRead(5)
	jumper2 = I2CIO8.digitalRead(6)
	jumper3 = I2CIO8.digitalRead(7)
	while True:
		for port in range(0,4):
			I2CIO8.digitalWrite(port,1)
			time.sleep(0.5)
			I2CIO8.digitalWrite(port,0)
		for port in range(2,0,-1):
			I2CIO8.digitalWrite(port,1)
			time.sleep(0.5)
			I2CIO8.digitalWrite(port,0)
		if I2CIO8.digitalRead(4) != jumper0:
			print("Jumper H5 changed")
			jumper0 = I2CIO8.digitalRead(4)
		if I2CIO8.digitalRead(5) != jumper1:
			print("Jumper H6 changed")
			jumper1 = I2CIO8.digitalRead(5)
		if I2CIO8.digitalRead(6) != jumper2:
			print("Jumper H7 changed")
			jumper2 = I2CIO8.digitalRead(6)
		if I2CIO8.digitalRead(7) != jumper3:
			print("Jumper H8 changed")
			jumper3 = I2CIO8.digitalRead(7)
