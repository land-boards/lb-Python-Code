# main.py -- put your code here!

from pyb import Pin

p_in = Pin('B3',Pin.PULL_UP)
value = p_in.value()
print(value)
