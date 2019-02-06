from tkinter import *
from time import *

# http://effbot.org/tkinterbook/canvas.htm

class MyFrame(Frame):
	def __init__(self):
		Frame.__init__(self)

		self.myCanvas = Canvas(width=640, height=480, bg="white")
		self.myCanvas.grid()

		my_rect_id = self.myCanvas.create_arc(150, 150, 300, 300, offset = "2,10", style="arc", width = 20)
		self.myCanvas.update()

frame02 = MyFrame()
frame02.mainloop()
