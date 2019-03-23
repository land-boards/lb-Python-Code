import utime
import machine
def blinkIt():
	pin2 = machine.Pin(2, machine.Pin.OUT)
	for loopCount in range(10):
		pin2.value(1)
		utime.sleep_ms(500)
		pin2.value(0)
		utime.sleep_ms(500)
		print("hello")

blinkIt()
