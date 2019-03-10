###############################################################################
# digio128 - DIGIO-128 library
###############################################################################

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

i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21),freq=400000)
outdata=bytearray(b'\x00')
for chipAddr in range(MCP23017_BASEADDR,MCP23017_BASEADDR+8):
	i2c.writeto_mem(chipAddr,MCP23017_IOCONA,outdata)	# set all bits to inputs
chipAddr = MCP23017_BASEADDR

def digitalWrite(bit,value): 	# Writes to a single bit
	global chipAddr
	chipAddr = MCP23017_BASEADDR | ((bit & 0x70) >> 4)
	if ((bit & 0x08) == 0):
		regAdr=MCP23017_OLATA
	else:
		regAdr=MCP23017_OLATB
	rwValue=readRegister(regAdr)
	if (value == 0):
		rwValue &= ~(1 << (bit&0x7))
	else:
		rwValue |= (1 << (bit&0x7))
	writeRegister(regAdr,rwValue)
	return

def digitalRead(bit):			# Reads a single bit
	global chipAddr
	chipAddr = MCP23017_BASEADDR | ((bit & 0x70) >> 4)
	if ((bit & 0x08) == 0):
		regAdr=MCP23017_GPIOA
	else:
		regAdr=MCP23017_GPIOB
	rdVal=readRegister(regAdr)
	return ((rdVal>>(bit&7))&0x01)

def pinMode(bit,value):			# Set the single bit direction (INPUT, INPUT_PULLUP, OUTPUT)
	global chipAddr
	chipAddr = MCP23017_BASEADDR | ((bit & 0x70) >> 4)
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
	readbackVal=bytearray(1)	# Allow buffer space
	i2c.readfrom_mem_into(chipAddr,regAdr,readbackVal)	# Do the read
	rwValue=readbackVal[0]	# Pull the first byte
	return rwValue				# Return value

def writeRegister(regAdr,wrValue):
	outBuff=bytearray(1)
	outBuff[0]=wrValue
	i2c.writeto_mem(chipAddr,regAdr,outBuff)	# Write to OLATA register
	return
	
# def blinkLED0():
	# pinMode(0,OUTPUT)
	# for loopCount in range(0,6):
		# digitalWrite(0,1)
		# time.sleep(0.25)
		# digitalWrite(0,0)
		# time.sleep(0.25)

# def fastToggle():
	# pinMode(0,OUTPUT)
	# for loopCount in range(0,6):
		# digitalWrite(0,1)
		# digitalWrite(0,0)

# blinkLED0()
