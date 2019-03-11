####################################################################
# blinkMcp23017Led.py - Blinks an LED on an MCP23017 partition
# Does not require libraries other than standard MicroPython libraries
# MCP23017 datasheet is
# http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf
####################################################################


import time
import machine

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))		# Set up pins
outdata=bytearray(b'\xfe') 				# IODIRA value lowest bit output
i2c.writeto_mem(0x20,0x00,outdata) 		# Set the IODIRA to output for lowest bit

def blinkLED0():
	for loopCount in range(0,10):
		outdata=bytearray(b'\x01') 			# Set LED high
		i2c.writeto_mem(0x20,0x14,outdata)	# Write to OLATA register
		time.sleep(0.25)
		outdata=bytearray(b'\x00')			# Set LED low
		i2c.writeto_mem(0x20,0x14,outdata)	# Write to OLATA register
		time.sleep(0.25)

blinkLED0()
