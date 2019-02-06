from tkinter import *
from time import *

class MyFrame(Frame):
	def __init__(self):
		Frame.__init__(self)

		self.myCanvas = Canvas(width=300, height=200, bg="white")
		self.myCanvas.grid()

		for count in range(10):
			increment = 10*count
			self.myCanvas.create_rectangle(10 + increment, 10 + increment, 50 + increment, 50 + increment)
			self.myCanvas.update()
			sleep(1)

frame02 = MyFrame()
frame02.mainloop()
