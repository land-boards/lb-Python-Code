###############################################################################
# testDigio32 - Test the digital IO lines with port-to-port loop cables
###############################################################################

import time
import digio32
import sys

def testDigio32():
	start = time.ticks_ms()
	print("Bounce LED on DIGIO32-I2C card")

	# Set all of the pins to pulled up inputs
	for bit in range(0,32):
		digio32.digitalWrite(bit,0)
		digio32.pinMode(bit,digio32.OUTPUT)
		if digio32.digitalRead(bit)!=0:
			print("testDigio32 (1): readback failed - expected 0, got 1")
			sys.exit(1)
		
	# Blink all LEDs
	for loopCount in range(0,10):
		for bit in range(0,32):
			digio32.digitalWrite(bit,1)
			time.sleep(0.5)
			if digio32.digitalRead(bit)!=1:
				print("testDigio32 (2): readback failed - expected 1, got 0")
				sys.exit(1)
			digio32.digitalWrite(bit,0)
	deltaTime = time.ticks_diff(start, time.ticks_ms())/1000
	print("Test completed, time =",abs(deltaTime))
