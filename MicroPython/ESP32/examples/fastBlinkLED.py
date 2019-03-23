import machine
def blinkIt():
	pin2 = machine.Pin(2, machine.Pin.OUT)
	while True:
		pin2.value(1)
		pin2.value(0)

blinkIt()
