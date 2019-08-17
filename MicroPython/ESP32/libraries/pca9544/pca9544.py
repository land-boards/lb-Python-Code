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

i2c=machine.I2C(scl=machine.Pin(22),sda=machine.Pin(21),freq=200000)		# Set up pins

def setI2CMuxPort(wrValue): 	# Writes to a single bit
	outBuff=bytearray(1)
	outBuff[0]=wrValue
	i2c.writeto(PCA9544_BASEADDR, outBuff)
	
setI2CMuxPort(4)	# 4 selects channel 0
