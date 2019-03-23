# readSwitchLightLED

import pyb
sw = pyb.Switch()

while True:
	if sw.value():
		pyb.LED(4).on()
	else:
		pyb.LED(4).off()
