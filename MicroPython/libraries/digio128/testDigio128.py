###############################################################################
# testDigio128 - Test the digital IO lines with port-to-port loop cables
###############################################################################

import time
import digio128
import sys

def testDigio128():
	start = time.ticks_ms()
	print("Testing DIGIO-128 card")
	# Set all of the pins to pulled up inputs
	for bit in range(0,128):
		digio128.pinMode(bit,digio128.INPUT_PULLUP)
	# verify all pins were set to pulled up inputs
	for bit in range(0,128):
		if digio128.digitalRead(bit) != 1:
			print("testDigio128(1): Expected pullup on input pin")
			sys.exit(1)
	# Write bits one at a time to 0
	for writtenBit in range(0,128):
		digio128.pinMode(writtenBit,digio128.OUTPUT)
		digio128.digitalWrite(writtenBit,0)
		loopBackBit=writtenBit^0x1f
		# Check all of the pins to be sure only one pin was set to 0
		for checkingBit in range(0,128):
			readValue = digio128.digitalRead(checkingBit)
			# The bit being tested should be 0
			if writtenBit == checkingBit:	# The bit being tested
				if readValue != 0:
					print("testDigio128(2): Expected a 0, got a 1")
					print("testDigio128(2): writtenBit =",writtenBit)
					print("testDigio128(2): checkingBit =",checkingBit)				
					print("testDigio128(2): readValue =",readValue)				
					print("testDigio128(2): loopBackBit =",loopBackBit)
					sys.exit(1)
			# The looped back bit should be 0
			elif checkingBit==loopBackBit:	# The loopback cable here
				if readValue!=0:
					print("testDigio128(3): Expected a 0, got a 1")
					print("testDigio128(3): writtenBit",writtenBit)
					print("testDigio128(3): checkingBit =",checkingBit)				
					print("testDigio128(3): readValue =",readValue)				
					print("testDigio128(3): Expected a 1, got a 0")
					print("testDigio128(3): loopBackBit =",loopBackBit)
					sys.exit(1)
				digio128.digitalWrite(writtenBit,1)
				if digio128.digitalRead(loopBackBit)!= 1:
					print("testDigio128(4): Expected a 1, got a 0")					
				digio128.digitalWrite(writtenBit,0)
			# All the other pins should be 1
			elif readValue!=1:
				print("testDigio128(5): writtenBit =",writtenBit)				
				print("testDigio128(5): checkingBit =",checkingBit)				
				print("testDigio128(5): readValue =",readValue)				
				print("testDigio128(5): Expected a 1, got a 0")
				print("testDigio128(5): loopBackBit =",loopBackBit)
				sys.exit(1)
		digio128.pinMode(writtenBit,digio128.INPUT_PULLUP)
	deltaTime = time.ticks_diff(start, time.ticks_ms())/1000
	print("Test passed, time =",abs(deltaTime))
