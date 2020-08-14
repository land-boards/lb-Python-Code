"""
pyCSVtoCSVTk.py
Convert a CSV into a different formatted CSV.
"""

import string
import sys
from sys import version_info

sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules\\TKDGCommon')

from dgProgDefaultsTk import *
from dgReadCSVtoListTk import *
from dgWriteListtoCSVTk import *

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

defaultPath = ''

verboseMode = False

def errorDialog(errorString):
	messagebox.showerror("Error", errorString)

def infoBox(msgString):
	messagebox.showinfo("pyFlattenPL_2",msgString)

class ControlClass:
	def __init__(self):
		self.errorsList = []
		self.defaultInfilePath = ''
		self.outPathFilename = ''
	
	def findReadCSVFile(self, startingPath):
		"""findReadCSVFile() - This is the dialog which locates the csv files
	
		:returns: path/name of the file that was selected
		"""
		global verboseMode
		inputCSVFileClass = ReadCSVtoList()
		inputCSVFileClass.setFreshCheckFlag(False)
		inputCSVFileClass.setVerboseMode(False)
		inputCSVFileClass.setUseSnifferFlag(False)
		inBOM = inputCSVFileClass.findOpenReadCSV(self.defaultInfilePath,'Select BOM')
		self.defaultInfilePath = inputCSVFileClass.getLastPath()
		self.outPathFilename = inputCSVFileClass.getLastPathFileName()
		return inBOM
		
	def createOutputFileName(self, inFileName):
		"""Creates the output file name based on the input file name
		
		:param inFIleName: The pathfilename of the input file.
		"""
		return(inFileName[0:-4] + '_out.csv')
		
	def writeOutputHeader(self, outPtr):
		"""Write out the Output header.
		
		:param outPtr: The pointer to the output CSV file.
		"""
		outPtr.writerow(['column1','column2'])
		return

	""" the stuff to open output file
	"""

	def writeOutputFile(self, outFile, outFilePtr):
		"""Write out header and body
		"""
		self.writeOutputHeader(outFilePtr)					# write out the header
		outFilePtr.writerows(outFile)						# write out the BOM list to the output CSV file
		
	def processCSV(self, theInList):
		''' This function is where the conversion from one CSV format to another happens
		List the input fields here
		...
		List the output fields here
		...
		'''
		myOutList = []
		for row in theInList:	# Go through the input list one line at a time
			myOutList.append(row)
		return myOutList
		
	def doConvert(self):
		'''This is the main executive which gets called when someone selects file open.
		'''
		theInList = self.findReadCSVFile('.')

		fileToWrite = self.outPathFilename[:-4] + "_out.csv"
		print('out file name', fileToWrite)

		try:
			outFile = open(fileToWrite, 'w')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(fileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		# Pointer to the CSV writer
		outFil = csv.writer(outFile)
		
		
		# Process the CSV file
		theOutList = self.processCSV(theInList)
		
		# Write out the CSV file
		self.writeOutputFile(theOutList, outFil)

class Dashboard:
	def __init__(self):
		self.win = Tk()
		self.win.geometry("320x240")
		self.win.title("pyCSVtoCSVTk.py")

	def add_menu(self):
		self.mainmenu = Menu(self.win)
		self.win.config(menu=self.mainmenu)

		self.filemenu = Menu(self.mainmenu, tearoff=0)
		self.mainmenu.add_cascade(label="File",menu=self.filemenu)

		self.filemenu.add_command(label="Open BOM file",command=control.doConvert)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit",command=self.win.quit)

		self.win.mainloop()

if __name__ == "__main__":
	if version_info.major != 3:
		errorDialog("Requires Python 3")
	control = ControlClass()
	x = Dashboard()
	x.add_menu()
