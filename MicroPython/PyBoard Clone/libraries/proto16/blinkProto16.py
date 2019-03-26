###############################################################################
# blinkProto16 - Blink the first LED
###############################################################################

import time
import mcp23017		# Land Board library which uses Arduino style functions
import sys

def blinkProto16():
	start = time.ticks_ms()
	print("Bounce LED on Proto16-I2C card")

	# Set all of the pins to inputs
	for bit in range(0,32):
		mcp23017.pinMode(bit,mcp23017.INPUT)
		
	# Blink first LED
	mcp23017.pinMode(0,mcp23017.OUTPUT)
	while True:
		mcp23017.digitalWrite(0,1)
		time.sleep(0.25)
		mcp23017.digitalWrite(0,0)
		time.sleep(0.25)
