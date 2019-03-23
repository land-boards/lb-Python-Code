###############################################################################
# testDigio32 - Test the digital IO lines with port-to-port loop cables
###############################################################################

import time
import digio32
import sys

def blinkDigio32():
	start = time.ticks_ms()
	print("Bounce LED on DIGIO32-I2C card")

	# Set all of the pins to inputs
	for bit in range(0,32):
		digio32.pinMode(bit,digio32.INPUT)
		
	# Blink all LEDs
	digio32.pinMode(0,digio32.OUTPUT)
	while True:
		digio32.digitalWrite(0,1)
		time.sleep(0.25)
		digio32.digitalWrite(0,0)
		time.sleep(0.25)
