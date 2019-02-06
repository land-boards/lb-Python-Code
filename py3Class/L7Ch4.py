from tkinter import *
from time import *

class MyFrame(Frame):
	def __init__(self):
		Frame.__init__(self)

		self.myCanvas = Canvas(width=300, height=200, bg="white")
		self.myCanvas.grid()

		self.myCanvas.create_rectangle(10, 10, 50, 50)
		self.myCanvas.update()

		sleep(1)

		self.myCanvas.create_rectangle(20, 20, 60, 60)

frame02 = MyFrame()
frame02.mainloop()
