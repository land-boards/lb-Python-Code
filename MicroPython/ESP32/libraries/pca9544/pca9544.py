###############################################################
# PCA9544 library
# Uses MicroPython machine I2C library as described
# http://docs.micropython.org/en/latest/library/machine.I2C.html
# PCA9544 datasheet is at
# http://www.ti.com/lit/ds/symlink/pca9544a.pdf
###############################################################

import time
import machine

PCA9544_BASEADDR=0x70
SELCH0 = 0X04	# Select mux channel #0
SELCH1 = 0X05	# Select mux channel #1
SELCH2 = 0X06	# Select mux channel #2
SELCH3 = 0X07	# Select mux channel #3

i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21),freq=200000)		# Set up pins

def setI2CMuxPort(wrValue): 	# Writes to a single bit
	outBuff=bytearray(1)
	if wrValue == 0:
		outBuff[0]=SELCH0
	elsif wrValue == 1:
		outBuff[0]=SELCH1
	elsif wrValue == 2:
		outBuff[0]=SELCH2
	elsif wrValue == 3:
		outBuff[0]=SELCH3
	i2c.writeto(PCA9544_BASEADDR, outBuff)
