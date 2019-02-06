from tkinter import *
""" 
Introduction to Python 3 Programming
Lesson 7: Creating Graphics With Tkinter
Lesson 7: Creating Graphics With Tkinter
Chapter 3: Canvas Shapes
"""
class MyFrame(Frame):
	def __init__(self):
		Frame.__init__(self)

		self.myCanvas = Canvas(width=640, height=480, bg="white")
		self.myCanvas.grid()
		# self.myCanvas.create_rectangle(10, 10, 100, 100, outline="black", fill="blue", width=4)
		# self.myCanvas.create_rectangle(10, 10, 200, 100, fill="blue")
		# self.myCanvas.create_oval(10, 10, 200, 100, fill="white")
		# self.myCanvas.create_line(1, 1, 200, 200, arrow="last")
		self.myCanvas.create_text(320, 240, text="Hello World",
			width=70, fill="blue", anchor="center",
			justify="center", font=("Times", 16))
		
frame02 = MyFrame()
frame02.mainloop()
