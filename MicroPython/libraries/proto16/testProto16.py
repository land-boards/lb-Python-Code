###############################################################################
# testProto16 - Test the digital IO lines with port-to-port loop cables
###############################################################################

import time
import mcp23017		# Land Board library which uses Arduino style functions
import sys

def testProto16():
	start = time.ticks_ms()
	print("Bounce LED on PROTO16-I2C card")

	# Set all of the pins to pulled up inputs
	for bit in range(0,16):
		mcp23017.digitalWrite(bit,0)
		mcp23017.pinMode(bit,mcp23017.OUTPUT)
		if mcp23017.digitalRead(bit)!=0:
			print("testProto16 (1): readback failed - expected 0, got 1")
			sys.exit(1)
		if mcp23017.digitalRead(bit)!=0:
			print("testProto16 (2): readback failed - expected 0, got 1")
			sys.exit(1)
		
	# Blink all LEDs
	for loopCount in range(0,10):
		for bit in range(0,32):
			mcp23017.digitalWrite(bit,1)
			time.sleep(0.5)
			if mcp23017.digitalRead(bit)!=1:
				print("testProto16 (3): readback failed - expected 1, got 0")
				sys.exit(1)
			mcp23017.digitalWrite(bit,0)
	deltaTime = time.ticks_diff(start, time.ticks_ms())/1000
	print("Test completed, time =",abs(deltaTime))
