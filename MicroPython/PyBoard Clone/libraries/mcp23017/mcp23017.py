###############################################################
# MCP23017 library
# Implements an Arduino style call library
# Uses MicroPython machine I2C library as described
# http://docs.micropython.org/en/latest/library/machine.I2C.html
# MCP23017 datasheet is
# http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf
###############################################################

import time
import machine

MCP23017_BASEADDR=0x20

# IOCON.BANK0
MCP23017_IODIRA=0x00
MCP23017_IPOLA=0x02
MCP23017_GPINTENA=0x04
MCP23017_DEFVALA=0x06
MCP23017_INTCONA=0x08
MCP23017_IOCONA=0x0A
MCP23017_GPPUA=0x0C
MCP23017_INTFA=0x0E
MCP23017_INTCAPA=0x10
MCP23017_GPIOA=0x12
MCP23017_OLATA=0x14

MCP23017_IODIRB=0x01
MCP23017_IPOLB=0x03
MCP23017_GPINTENB=0x05
MCP23017_DEFVALB=0x07
MCP23017_INTCONB=0x09
MCP23017_IOCONB=0x0B
MCP23017_GPPUB=0x0D
MCP23017_INTFB=0x0F
MCP23017_INTCAPB=0x11
MCP23017_GPIOB=0x13
MCP23017_OLATB=0x15

INPUT=0x0
OUTPUT=0x1
INPUT_PULLUP=0x2

i2c=machine.I2C(1)		# Set up pins
outdata=bytearray(b'\x00') 				# IODIRA value lowest bit output
i2c.writeto_mem(0x20,MCP23017_IOCONA,outdata) 		# Set the IODIRA to output for lowest bit

def digitalWrite(bit,value): 	# Writes to a single bit
	if ((bit & 0x08) == 0):
		regAdr=MCP23017_OLATA
	else:
		regAdr=MCP23017_OLATB
	# Need to do a read-modify-write to not mess up other bits
	rwValue=readRegister(regAdr)
	if (value == 0):
		rwValue &= ~(1 << (bit&0x7))
	else:
		rwValue |= (1 << (bit&0x7))
	writeRegister(regAdr,rwValue)
	return

def digitalRead(bit):			# Reads a single bit
	if ((bit & 0x08) == 0):
		regAdr=MCP23017_GPIOA
	else:
		regAdr=MCP23017_GPIOB
	rdVal=readRegister(regAdr)
	return ((rdVal>>(bit&7))&0x01)

def pinMode(bit,value):			# Set the single bit direction (INPUT, INPUT_PULLUP, OUTPUT)
	changeBit = 1 << (bit & 0x7)
	if ((bit & 0x08) == 0):
		puRegAdr=MCP23017_GPPUA
		dirRegAdr=MCP23017_IODIRA
	else:
		puRegAdr=MCP23017_GPPUB
		dirRegAdr=MCP23017_IODIRB
	rdPuVal=readRegister(puRegAdr)
	rdDirVal=readRegister(dirRegAdr)
	if (value == INPUT_PULLUP): 
		rdPuVal |= changeBit
		writeRegister(puRegAdr,rdPuVal)
		rdDirVal |= changeBit
		writeRegister(dirRegAdr,rdDirVal)
	elif (value == INPUT):
		rdPuVal &= ~changeBit
		writeRegister(puRegAdr,rdPuVal)
		rdDirVal |= changeBit
		writeRegister(dirRegAdr,rdDirVal)
	elif (value == OUTPUT):
		rdDirVal &= ~changeBit
		writeRegister(dirRegAdr,rdDirVal)

def readRegister(regAdr):
	#print("readRegister() - regAdr=",regAdr)
	readbackVal=bytearray(1)	# Allow buffer space
	i2c.readfrom_mem_into(0x20,regAdr,readbackVal)	# Do the read
	rwValue=readbackVal[0]	# Pull the first byte
	#print("readRegister() - rwValue=",rwValue)
	return rwValue				# Return value

def writeRegister(regAdr,wrValue):
	#print("writeRegister() - regAdr=",regAdr)
	#print("writeRegister() - wrValue=",wrValue)
	outBuff=bytearray(1)
	outBuff[0]=wrValue
	#print("writeRegister() - outBuff=",outBuff)
	i2c.writeto_mem(0x20,regAdr,outBuff)	# Write to OLATA register
	return
