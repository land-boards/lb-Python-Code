from tkinter import *


class Dashboard:
    def __init__(self):
        self.win = Tk()
        self.win.geometry("600x400")
        self.win.title("Dashboard")

    def add_menu(self):
        self.mainmenu = Menu(self.win)
        self.win.config(menu=self.mainmenu)

        self.filemenu = Menu(self.mainmenu)
        self.mainmenu.add_cascade(label="File",menu=self.filemenu)

        self.filemenu.add_command(label='New')
        self.filemenu.add_command(label="Open..")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",command=self.win.quit)

        self.editmenu = Menu(self.mainmenu)
        self.mainmenu.add_cascade(label="Edit",menu=self.editmenu)

        self.editmenu.add_command(label="Find")
        self.editmenu.add_command(label="Replace")

        self.win.mainloop()


if __name__ == "__main__":
    x = Dashboard()
    x.add_menu()