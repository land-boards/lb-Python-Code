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

def readEEPROM_8bits(memAdr):
	"""readEEPROM_8bits - read a single byte from the EEPROM
	
	:param memAdr: EEPROM 8-bit memory address (0-0xff)
	:returns: Character that was read from the EEPROM
	"""
	readbackVal=bytearray(1)
	i2c.readfrom_mem_into(boardBaseAddress + EEPROMAddress,memAdr,readbackVal)
	rwValue=readbackVal[0]
	return rwValue
	
def writeEEPROM_8bits(memAdr,wrValue):
	"""writeEEPROM_8bits
	
	:param memAdr: EEPROM 8-bit memory address (0-0xff)
	:param wrValue: Write value
	:returns: no return value
	"""
	outBuff=bytearray(1)
	outBuff[0]=wrValue
	i2c.writeto_mem(0x20,memAdr,outBuff)
	return

def readEEPROM_String(memAdr,length):
	"""readEEPROM_String - Read in a string from the EEPROM
	Reads in the number of bytes or stops when a null (0x0) is reached
	
	:param memAdr: EEPROM 8-bit memory address (0-0xff)
	:param length: Number of bytes to read
	:returns: String that was read from the EEPROM - null terminated
	"""
	retString = ''
	lenCounter = length
	adrEEPROM = memAdr
	for x in range(length):
		retChar = readEEPROM_8bits(adrEEPROM)
		retString += retChar
		if retChar == 0x0:
			return retString
	return retString
	
def writeEEPROM_String(memAdr,stringToWrite):
	"""writeEEPROM_String
	
	:param memAdr: EEPROM 8-bit memory address (0-0xff)
	:param stringToWrite: The string that is being written to EEPROM
	:returns: no return value
	"""
	adrEEPROM = memAdr
	for charToWrite in stringToWrite:
		writeEEPROM_8bits(adrEEPROM,charToWrite)
		adrEEPROM += 1

def testEEPROM():
	"""testEEPROM - Test the EEPROM
	Check a couple of locations to make sure they can be written and read back
	"""
	writeEEPROM_8bits(0,0xde)
	writeEEPROM_8bits(1,0xad)
	rdVal = readEEPROM_8bits(0)
	if rdVal != 0xde:
		print("testEEPROM(1): Write 0xde, read back", rdVal)
		exit()
	rdVal = readEEPROM_8bits(1)
	if rdVal != 0xad:
		print("testEEPROM(2): Write 0xad, read back", rdVal)
		exit()
