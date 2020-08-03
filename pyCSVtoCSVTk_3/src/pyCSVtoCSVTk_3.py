"""
pyCSVtoCSVTk_3.py
Convert a CSV into a different formatted CSV.
"""

import string
import csv
import sys
from sys import version_info
sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules\\TKDGCommon')

from dgProgDefaultsTk import *
from dgReadCSVtoListTk import *
from dgWriteListtoCSVTk import *

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

# global program options
progName = 'pyAdobePLtoAACPLCSV.py'
progVer = '0.0.1'

from sys import argv

def errorDialog(errorString):
	messagebox.showerror("Error", errorString)

def infoBox(msgString):
	messagebox.showinfo("pyFlattenPL_2",msgString)

class ControlClass:
	def findCSVFileBrowse(self, startingPath):
		"""findCSVFileBrowse() - This is the dialog which locates the csv files
	
		:returns: path/name of the file that was selected
		"""
		csvFileString = "Select file"
		dialog = gtk.FileChooserDialog(csvFileString,
			None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		if startingPath != '':
			dialog.set_current_folder(startingPath)
		filter = gtk.FileFilter()
		filter.set_name("CSV files")
		filter.add_pattern("*.csv")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFileName = dialog.get_filename()
			dialog.destroy()
			return retFileName
		elif response == gtk.RESPONSE_CANCEL:
			errorDialog("Closed, no files selected")
			dialog.destroy()
			exit()
		dialog.destroy()

	def readInCSV(self, inFile):
		csvReader = csv.reader(inFile)
		list2Read = []
		for row in csvReader:
			list2Read.append(row)
		return list2Read
		
	def createOutputFileName(self, inFileName):
		"""Creates the output file name based on the input file name
		
		:param inFIleName: The pathfilename of the input file.
		"""
		return(inFileName[0:-4] + '_CAN.csv')
		
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
		
	def validateHeader(self, theInList):
		"""validateHeader - Examine the header lines and check some spots

		:returns: True if the list conforms to the expected values, False if errors
		"""
		return True
	
	def mapHeader(self,headerRow):
		"""
		['Level', 'FIND NO', 'REF DES', '', 'QTY', 'UOM', 'CAGE CODE', 'NOTES', '', 'PART NO', '', '', '', '', '', '', 'REV', '', 'NOMENCLATURE OR DESCRIPTION', 
		'', '', '', '', '', 'CAV', 'ESD', 'PLANNING CODE', '', 'MFG CAGE', '', 'MFG PART NO', 'MFG REV', '']
		"""
		global findColumnNumber
		global qtyColumnNumber
		global umColumnNumber
		global cageColumnNumber
		global partnumberColumnNumber
		global revColumnNumber
		global dwgnumberColumnNumber
		global descrColumnNumber
		global refdesColumnNumber
		global notesColumnNumber
		global mbColumnNumber
		global mfgCAGEColumnNumber
		global mfgPNColumnNumber
		global mfgRevColumnNumber
		colOrd = 0
		for column in headerRow:
			if column == 'FIND NO':
				findColumnNumber = colOrd
			elif column == 'REF DES':
				 refdesColumnNumber = colOrd
			elif column == 'QTY':
				 qtyColumnNumber = colOrd
			elif column == 'UOM':
				 umColumnNumber = colOrd
			elif column == 'CAGE CODE':
				 cageColumnNumber = colOrd
			elif column == 'NOTES':
				 notesColumnNumber = colOrd
			elif column == 'PART NO':
				 partnumberColumnNumber = colOrd
			elif column == 'REV':
				 revColumnNumber = colOrd
			elif column == 'NOMENCLATURE OR DESCRIPTION':
				 descrColumnNumber = colOrd
			elif column == 'MFG CAGE':
				 mfgCAGEColumnNumber = colOrd
			elif column == 'MFG PART NO':
				 mfgPNColumnNumber = colOrd
			elif column == 'MFG REV':
				 mfgRevColumnNumber = colOrd
			colOrd += 1
	
	def processCSV(self, theInList):
		""" processCSV - This function is where the conversion from one CSV format to another happens
		"""
		myOutList = []
		return myOutList
		
	def doConvert(self):
		'''This is the main executive which gets called when someone selects file open.
		'''
		"""This method is the executive which calls the other functions.
		Load the default path file.
		Read in the BOM file and update the default path file.
		Read in the Attachment file.
		Compare the two files and make a list of the differences.
		Write out list of differences.
		"""
		global defaultPath
		#Load the default path
		defaultParmsClass = HandleDefault()
		#defaultParmsClass.setVerboseMode(False)
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		
		#Load the file
		myCSVFileReadClass = ReadCSVtoList()	# CSV reading class
		myCSVFileReadClass.setVerboseMode(False)
		theInList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select Input CSV BOM File')				# read BOM into list
		if theInList == []:
			return False
		
		# print("theInList"),
		# for row in theInList:
			# print(row)
		if not self.validateHeader(theInList):
			errorDialog("Unexpected Header value")
			return
		else:
			outList = self.processCSV(theInList)
		
		# Write out the deltas list
		outPathFilename = myCSVFileReadClass.getLastPathFileName()
		myWriteOut = WriteListtoCSV()
		
		#Write out the Cleaned up indented ExtAll format BOM file
		myWriteOut.appendOutFileName('_Out.csv')
		myWriteOut.setVerboseMode(True)
		newHeader = ['FIND','QTY','UM','CAGE','PARTNUMBER','REV','DWGNUMBER','DESCRIPTION','REFDES','NOTES','M/B']
		myWriteOut.writeOutList(outPathFilename, newHeader, outList)
		outPathFilename = myCSVFileReadClass.getLastPathFileName()
		
		infoBox("Completed")

	def runWithCmdlineFileName(self,inFileName):
		myCSVFileReadClass = ReadCSVtoList()	# CSV reading class
		myCSVFileReadClass.setVerboseMode(False)
		theInList = myCSVFileReadClass.readInCSV(inFileName)	# read BOM into list
		if theInList == []:
			return False
		if not self.validateHeader(theInList):
			errorDialog("Unexpected Header value")
			return
		else:
			outList = self.processCSV(theInList)
		
		# Write out the deltas list
		outPathFilename = inFileName
		myWriteOut = WriteListtoCSV()
		
		#Write out the Cleaned up indented ExtAll format BOM file
		myWriteOut.appendOutFileName('_Out.csv')
		myWriteOut.setVerboseMode(True)
		newHeader = ['FIND','QTY','UM','CAGE','PARTNUMBER','REV','DWGNUMBER','DESCRIPTION','REFDES','NOTES','M/B']
		myWriteOut.writeOutList(outPathFilename, newHeader, outList)
		outPathFilename = myCSVFileReadClass.getLastPathFileName()
		
		print("Completed")
		
	
class Dashboard:
	def __init__(self):
		self.win = Tk()
		self.win.geometry("320x240")
		windowTitle = progName + " Rev " + progVer
		self.win.title(windowTitle)

	def add_menu(self):
		self.mainmenu = Menu(self.win)
		self.win.config(menu=self.mainmenu)

		self.filemenu = Menu(self.mainmenu)
		self.mainmenu.add_cascade(label="File",menu=self.filemenu)

		self.filemenu.add_command(label="Open CSV BOM",command=control.doConvert)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit",command=self.win.quit)

		self.win.mainloop()

if __name__ == "__main__":
	print('Number of arguments:', len(sys.argv), 'arguments.')
	print('Argument List:', str(sys.argv))
	if len(sys.argv) == 1:
		if version_info.major != 3:
			errorDialog("Requires Python 3")
		control = ControlClass()
		x = Dashboard()
		x.add_menu()
	else:
		print("Running from command line")
		control = ControlClass()
		control.runWithCmdlineFileName(sys.argv[1])
		