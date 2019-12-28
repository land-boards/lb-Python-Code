# !/usr/bin/python3
from tkinter import *

root = Tk()

root.option_add('*tearOff', False)
menubar = Menu(root)
root.config(menu=menubar)
file = Menu(menubar)
edit = Menu(menubar)
help_ = Menu(menubar)
menubar.add_cascade(menu=file, label='File')
menubar.add_cascade(menu=edit, label='Edit')
menubar.add_cascade(menu=help_, label='Help')
file.add_command(label='New', command=lambda: print('New File'))

file.add_separator()
file.add_command(label='Open...', command=lambda: print('Opening File...'))
file.entryconfig('New', accelerator='Ctrl + N')
logo = PhotoImage(file='C:\\Users\\Paopao\\Pictures\\python.gif').subsample(10, 10)
file.entryconfig('Open...', image=logo, compound='left')
file.entryconfig('Open...', state='disabled')
save = Menu(file)
file.add_cascade(menu=save, label='Save')
save.add_command(label='Save As', command=lambda: print('Saving As...'))
save.add_command(label='Save All', command=lambda: print('Saving All...'))

choice = IntVar()
edit.add_radiobutton(label="One", variable=choice, value=1)
edit.add_radiobutton(label="Two", variable=choice, value=2)
edit.add_radiobutton(label="Three", variable=choice, value=3)

if __name__ == '__main__':
    mainloop()
