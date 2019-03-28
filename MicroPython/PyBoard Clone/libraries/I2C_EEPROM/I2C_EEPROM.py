# I2C_EEPROM Methods
# MicroPython
# EEPROM access are similar to the indirect accesses like the MCP23017
# They require read from/to memory calls
# 24LC024 EEPROM is organized as a single block of 256 bytes (256 x 8)
# This simplifies the addressing since only a single 8-bit address is needed
# Larger EEPROMs will have different addressing schemes

import time
import machine

boardBaseAddress = 0x0
EEPROMAddress = 0x50

i2c=machine.I2C(1)		# Set up pins

def readEEPROM(memAdr):
	readbackVal=bytearray(1)
	i2c.readfrom_mem_into(boardBaseAddress + EEPROMAddress,memAdr,readbackVal)
	rwValue=readbackVal[0]
	return rwValue
	
def writeEEPROM(memAdr,wrValue):
	outBuff=bytearray(1)
	outBuff[0]=wrValue
	i2c.writeto_mem(0x20,memAdr,outBuff)
	return

def testEEPROM():
	writeEEPROM(0,0xde)
	writeEEPROM(1,0xad)
	rdVal = readEEPROM(0)
	if rdVal != 0xde:
		print("testEEPROM(1): Write 0xde, read back", rdVal)
		exit()
	rdVal = readEEPROM(1)
	if rdVal != 0xad:
		print("testEEPROM(2): Write 0xad, read back", rdVal)
		exit()
