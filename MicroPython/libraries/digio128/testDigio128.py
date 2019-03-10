###############################################################################
# digio128 - DIGIO-128 library
###############################################################################

import time
import machine
import digio128
import sys
#import math

def testDigio128():
	start = time.ticks_ms()
	print("Testing DIGIO-128 card")
	for bit in range(0,128):
		digio128.pinMode(bit,digio128.INPUT_PULLUP)
	for readBit in range(0,128):
		if digio128.digitalRead(readBit) != 1:
			print("testDigio128(1): Expected pullup on input pin")
			sys.exit(1)
	for testingBit in range(0,128):
		digio128.pinMode(bit,digio128.OUTPUT)
		digio128.digitalWrite(testingBit,0)
		loopBackBit=testingBit^0x1f
		for checkingBit in range(0,128):
			readValue = digio128.digitalRead(checkingBit)
			if testingBit == checkingBit:	# The bit being tested
				if readValue == 0:
					print("testDigio128(2): Expected a 0, got a 1")
					print("testDigio128(2): testingBit",testingBit)
					sys.exit(1)
			elif testingBit == loopBackBit:	# The loopback cable here
				if readValue != 0:
					print("testDigio128(3): Expected a 0, got a 1")
					print("testDigio128(3): testingBit",testingBit)
					sys.exit(1)
				digio128.digitalWrite(testingBit,1)
				if digio128.digitalRead(loopBackBit)!= 1:
					print("testDigio128(4): Expected a 1, got a 0")					
				digio128.digitalWrite(testingBit,0)
			elif readValue!=1:
				print("testDigio128(5): testingBit =",testingBit)				
				print("testDigio128(5): checkingBit =",checkingBit)				
				print("testDigio128(5): readValue =",readValue)				
				print("testDigio128(5): Expected a 1, got a 0")
				print("testDigio128(5): loopBackBit =",loopBackBit)
				sys.exit(1)
		digio128.pinMode(bit,digio128.INPUT_PULLUP)
	deltaTime = time.ticks_diff(start, time.ticks_ms())/1000
	print("Test passed, time =",abs(deltaTime))
