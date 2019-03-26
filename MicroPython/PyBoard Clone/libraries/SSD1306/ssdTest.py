# ssd1306 example
# Frame buffer library
# http://docs.micropython.org/en/latest/library/framebuf.html
# 

import machine, ssd1306
i2c = machine.I2C(1)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 60)
oled.fill(0)
oled.text("Hello World", 0, 0)
oled.show()
