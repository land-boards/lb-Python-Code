# !/usr/bin/python3
from tkinter import *
from tkinter import filedialog

def donothing():
	filewin = Toplevel(root)
	button = Button(filewin, text="Do nothing button")
	button.pack()

def browse_to_folder():
	dirname = filedialog.askdirectory()
	print (dirname)

def open_file():
	filename = filedialog.askopenfilename()
	print (dirname)

def save_as_file():
	filename = filedialog.asksaveasfilename()
	print (dirname)

root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
# filemenu.add_command(label="New", command = donothing)
filemenu.add_command(label = "Select Folder", command = browse_to_folder)
# filemenu.add_command(label = "Save", command = donothing)
filemenu.add_command(label = "Save as...", command = save_as_file)
# filemenu.add_command(label = "Close", command = donothing)

filemenu.add_separator()

filemenu.add_command(label = "Exit", command = root.quit)
menubar.add_cascade(label = "File", menu = filemenu)
# editmenu = Menu(menubar, tearoff=0)
# editmenu.add_command(label = "Undo", command = donothing)

# editmenu.add_separator()

# editmenu.add_command(label = "Cut", command = donothing)
# editmenu.add_command(label = "Copy", command = donothing)
# editmenu.add_command(label = "Paste", command = donothing)
# editmenu.add_command(label = "Delete", command = donothing)
# editmenu.add_command(label = "Select All", command = donothing)

# menubar.add_cascade(label = "Edit", menu = editmenu)
helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label = "Help Index", command = donothing)
helpmenu.add_command(label = "About...", command = donothing)
menubar.add_cascade(label = "Help", menu = helpmenu)

root.config(menu = menubar)
root.mainloop()