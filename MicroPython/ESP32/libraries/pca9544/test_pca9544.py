###############################################################
# test_pca9544
# Uses MicroPython machine I2C library as described
# http://docs.micropython.org/en/latest/library/machine.I2C.html
# PCA9544 datasheet is at
# http://www.ti.com/lit/ds/symlink/pca9544a.pdf
###############################################################

import machine

PCA9544_BASEADDR=0x70

SELCH0 = 0X04	# Select mux channel #0
SELCH1 = 0X05	# Select mux channel #1
SELCH2 = 0X06	# Select mux channel #2
SELCH3 = 0X07	# Select mux channel #3

MCP23008_BASEADDR=0x20

MCP23008_IODIR=0x00
MCP23008_IPOL=0x01
MCP23008_GPINTEN=0x02
MCP23008_DEFVAL=0x03
MCP23008_INTCON=0x04
MCP23008_IOCON=0x05
MCP23008_GPPU=0x06
MCP23008_INTF=0x07
MCP23008_INTCAP=0x08
MCP23008_GPIO=0x09
MCP23008_OLAT=0x0A

INPUT=0x0
OUTPUT=0x1
INPUT_PULLUP=0x2

i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21),freq=400000)
outBuff=bytearray(b'\x04')		# Set I2C port hub
i2c.writeto(PCA9544_BASEADDR,outBuff)
outdata=bytearray(b'\xf0')
i2c.writeto_mem(MCP23008_BASEADDR,MCP23008_IOCON,outdata)
i2c.writeto_mem(MCP23008_BASEADDR,MCP23008_IODIR,outdata)
i2c.writeto_mem(MCP23008_BASEADDR,MCP23008_IPOL,outdata)
i2c.writeto_mem(MCP23008_BASEADDR,MCP23008_GPINTEN,outdata)
outdata=bytearray(b'\x00')
i2c.writeto_mem(MCP23008_BASEADDR,MCP23008_GPIO,outdata)
i2c.writeto_mem(MCP23008_BASEADDR,MCP23008_INTCON,outdata)

def digitalWrite(bit,value): 	# Writes to a single bit
	# Need to do a read-modify-write to not mess up other bits
	rwValue=readRegister(MCP23008_OLAT)
	if (value == 0):
		rwValue &= ~(1 << (bit&0x7))
	else:
		rwValue |= (1 << (bit&0x7))
	writeRegister(MCP23008_OLAT,rwValue)
	return

def digitalRead(bit):			# Reads a single bit
	rdVal=readRegister(MCP23008_GPIO)
	return ((rdVal>>(bit&7))&0x01)

def pinMode(bit,value):			# Set the single bit direction (INPUT, INPUT_PULLUP, OUTPUT)
	changeBit = 1 << (bit & 0x7)
	puRegAdr=MCP23008_GPPU
	dirRegAdr=MCP23008_IODIR
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
	i2c.readfrom_mem_into(MCP23008_BASEADDR,regAdr,readbackVal)	# Do the read
	rwValue=readbackVal[0]	# Pull the first byte
	#print("readRegister() - rwValue=",rwValue)
	return rwValue				# Return value

def writeRegister(regAdr,wrValue):
	#print("writeRegister() - regAdr=",regAdr)
	#print("writeRegister() - wrValue=",wrValue)
	outBuff=bytearray(1)
	outBuff[0]=wrValue
	#print("writeRegister() - outBuff=",outBuff)
	i2c.writeto_mem(MCP23008_BASEADDR,regAdr,outBuff)	# Write to OLATA register
	return
