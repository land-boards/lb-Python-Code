"""
=================
pyCSVtoMWTable.py
=================

Convert a CSV into a MediaWiki table.

==========
Background
==========

MediaWiki is a very common Wiki page format. 
Wikipedia is the primary example that comes to mind for MediaWiki.
htt;://land-boards.com/blwiki is another popular page.

We wanted a way to easily load tables into Media Wiki.
The tables were in .csv (EXCEL) format.

=====
Usage
=====

This program prompts for a path and file to select for input.
The output file is created in the same path with a .MW output file name.

Uses Python 3 and Tkinter.

===
API
===

"""
from __future__ import print_function

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

import csv
#import string
import os
import sys

sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules\\TKDGCommon')
sys.path.append('C:\\Users\\HPz420\\Documents\\GitHub\\land-boards\\lb-Python-Code\\dgCommonModules\\TKDGCommon')

from dgProgDefaultsTK import *
from dgReadCSVtoListTK import *
defaultPath = '.'

from sys import argv

def errorDialog(errorString):
	messagebox.showerror("Error", errorString)

def infoBox(msgString):
	messagebox.showinfo("pyCSVtoMWTable",msgString)

class ControlClass(object):
	def theExecutive(self):
		"""
		:global lastPathFileName: The path and file name that was found by the browser.

		The code that calls the other code.
		This code uses the defaults library to handle the default path.
		This code uses the read CSV library to read in the CSV file.
		"""
		global defaultPath
		
		defaultParmsClass = HandleDefault()
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		#print 'defaultPath',defaultPath

		myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
		myCSVFileReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		theInList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select CSV File')	# read in CSV into list
		if theInList == []:
			return False
		fileToWrite = myCSVFileReadClass.getLastPathFileName()[0:-4] + '.MW'
		#print 'fileToWrite',fileToWrite
		try:
			outFile = open(fileToWrite, 'w')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(fileToWrite, 'w')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		self.writeOutMWTable(outFile, theInList)
		infoBox("Finished")
		
	def writeOutMWTable(self, outFilePtr, theList):
		"""
		:param outFilePtr: Points to the output file.
		:param theList: The list to write out.

		"""
		outFilePtr.write('{| class="wikitable"\n')
		firstRow = True
		for row in theList:
			for cell in row:
				if firstRow:
					outFilePtr.write('! ' + cell + '\n')					
				else:
					outFilePtr.write('| ' + cell + '\n')
			firstRow = False
			outFilePtr.write('|-\n')
		outFilePtr.write('|}\n')

class Dashboard:
	def __init__(self):
		self.win = Tk()
		self.win.geometry("320x240")
		self.win.title("pyCSVtoMWTable")

	def add_menu(self):
		self.mainmenu = Menu(self.win)
		self.win.config(menu=self.mainmenu)

		self.filemenu = Menu(self.mainmenu)
		self.mainmenu.add_cascade(label="File",menu=self.filemenu)

		self.filemenu.add_command(label="Open CSV PL file",command=control.theExecutive)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit",command=self.win.quit)

		self.win.mainloop()

if __name__ == "__main__":
	control = ControlClass()
	x = Dashboard()
	x.add_menu()
