import pyb
leds = [pyb.LED(i) for i in range(1,5)]
n = 0
while True:
  n = (n + 1) % 4
  leds[n].toggle()
  pyb.delay(250)