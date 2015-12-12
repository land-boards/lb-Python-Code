"""
pyPayPal.py
Convert a PayPal CSV history into separate cost Accounts.
"""

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	 print "PyGtk 2.3.90 or later required"
	 raise SystemExit

import csv
import string
import sys
import os

from sys import argv

pathToFile = '.'
defaultPath = '.'
defaultsFileNamePath = '.\\Defaults.csv'
outFileName = ''

def errorDialog(errorString):
	"""
	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class HandleDefault:
	""""Load and save defaults file
	This can be used to save stuff like the default path
	The file is a simple list with KEY, value pairs on individual lines
	"""
	global defaultsFileNamePath
	def loadDefaults(self):
		""" Load the defaults file
		"""
		defaultFileHdl = open(defaultsFileNamePath, 'rb')
		defaultListItem = csv.reader(defaultFileHdl)
		defaultList = []
		for row in defaultListItem:
			defaultList+=row
		return defaultList

	def getKeyVal(self, keyName):
		"""feed it a key name and it returns the corresponding key value
		:param: keyName - the name of the key to look up
		:return: the value of that key, blank if there is no corresponding key
		"""
		if self.ifExistsDefaults() == False:
			self.createDefaults()
		defaultFileHdl = open(defaultsFileNamePath, 'rb')
		defaultListItem = csv.reader(defaultFileHdl)
		defaultList = []
		for row in defaultListItem:
			if row[0] == keyName:
				return row[1]
		return ''
	
	def storeDefaults(self,defaultList):
		""" Store to the defaults file
		"""
#		print 'storing list', defaultList
		defaultFileHdl = open(defaultsFileNamePath, 'wb')
		defaultFile = csv.writer(defaultFileHdl)
		defaultFile.writerows(defaultList)
		return True

	def createDefaults(self):
		""" Create the defaults file
		"""
		defaultFileHdl = open(defaultsFileNamePath, 'wb')
		defaultFile = csv.writer(defaultFileHdl)
		defaultArray = ['DEFAULT_PATH','.']
		defaultFile.writerow(defaultArray)
		return True
		
	def ifExistsDefaults(self):
		""" Check if the defaults file exists
		
		:return: True if the default file exists, false if the default file does not exist
		"""
		try:
			open(defaultsFileNamePath)
		except:
			return False
		return True

	def checkSetDefaults(self):
		"""Checks to see if there is a defaults file.
		If there is not a defaults file it creates a basic defaults file with a path to the data files.
		Opens the defaults file and loads the path into the global variable defaultPath
		
		:global: defaultPath default path of the data files.
		"""
		global defaultPath
		if self.ifExistsDefaults() == True:
			detailParmList = self.loadDefaults()
			print 'loaded defaults file'
		else:
			print 'defaults file does not exist'
			self.createDefaults()
			print 'created defaults file'
			detailParmList = self.loadDefaults()
			print 'loaded defaults file'
		if detailParmList[0] != 'DEFAULT_PATH':
			print 'Expected the first line to say DEFAULT_PATH, got',detailParmList
			defaultPath = '.'
		else:
			print 'default path is', detailParmList[1]
			defaultPath = detailParmList[1]

class WriteOutToCSVFile:
	"""writing out a CSV file
	"""
	def openCSVFileForWrites(self, csvName):
		"""Open the CSV file for output.
		
		:param csvName: the name of the file as a string
		"""
		try:
			myCSVFile = open(csvName, 'wb')
		except:
			print "Couldn't open\nIs the file open in EXCEL?, Try closing the file"
			s = raw_input('Hit enter to continue --> ')
			try:
				myCSVFile = open(csvName, 'wb')
			except:
				print "Couldn't open\nIs the file STILL open in EXCEL?\nExiting..."
				s = raw_input('Hit enter to exit --> ')
				exit()
		outFil = csv.writer(myCSVFile)
		return(outFil)

	def writeOutCsvBody(self, theOutList, outFileName):
		"""write out the CSV body
		
		:param theOutList: list that needs to be written out
		:param outFileName: string that has the pathfilename
		"""

	def doWriteOut(self, outFileName, theOutList):
		"""Calls the other function which do the write out of the CSV file
	
		:param outFileName: string which has the pathfilename
		:param theOutList: the list to write out
		"""
		outFilePtr = self.openCSVFileForWrites(outFileName)			# start at the same folder as the input file was located
#		self.writeOutputHeader(theOutList, outFilePtr)		# write out the header
		outFilePtr.writerows(theOutList)					# write out the BOM list to the output CSV file
			
class FindCSVFile:
	def findCSVFileBrowse(self, startingPath):
		"""findCSVFileBrowse() - This is the dialog which locates the csv files
	
		:returns: path/name of the file that was selected
		"""
		global defaultPath
		csvFileString = "Select orders.csv file"
		dialog = gtk.FileChooserDialog(csvFileString,
			None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

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
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
		dialog.destroy()

class ControlClass:
	def readInCSVToList(self, inFile):
		"""Read in a CSV file into a list
		"""
		csvReader = csv.reader(inFile)
		list2Read = []
		for row in csvReader:
			list2Read.append(row)
		return list2Read

	def findTransactionTypes(self,fromList):
		"""
		"""
		transactionTypesList = []
		for row in fromList[1:]:
			if row[4] not in transactionTypesList:
				transactionTypesList.append(row[4])
		return transactionTypesList

	def sumCategories(self, fromList, transTypes):
		categorySums = []
		categoryItem = ['Transaction Type','Total']
		categorySums.append(categoryItem)
		for tranItem in transTypes:
			grossTotal = 0.0
			for row in fromList[1:]:
				if tranItem == row[4]:
					grossTotal += float(row[7])
			categoryItem = []
			categoryItem.append(tranItem)
			categoryItem.append(grossTotal)
			categorySums.append(categoryItem)
		return categorySums
	
	def processList(self, theFromList):
		'''processList
		Turns a list from one format to another.
		Input list format: Date, Time, Time Zone, Name, Type, Status, Currency, Gross, Fee, Net, From Email Address, To Email Address, Transaction ID, Counterparty Status, Shipping Address, Address Status, Item Title, Item ID, Shipping and Handling Amount, Insurance Amount, Sales Tax, Option 1 Name, Option 1 Value, Option 2 Name, Option 2 Value, Auction Site, Buyer ID, Item URL, Closing Date, Escrow Id, Invoice Id, Reference Txn ID, Invoice Number, Custom Number, Receipt ID, Balance, Contact Phone Number, 
		Output list format: Date, Time, Time Zone, Name, Type, Status, Currency, Gross, Fee, Net, From Email Address, To Email Address, Transaction ID, Counterparty Status, Shipping Address, Address Status, Item Title, Item ID, Shipping and Handling Amount, Insurance Amount, Sales Tax, Option 1 Name, Option 1 Value, Option 2 Name, Option 2 Value, Auction Site, Buyer ID, Item URL, Closing Date, Escrow Id, Invoice Id, Reference Txn ID, Invoice Number, Custom Number, Receipt ID, Balance, Contact Phone Number, 
		
		'''
		transTypeList = self.findTransactionTypes(theFromList)
		
		categorySumsList = self.sumCategories(theFromList,transTypeList)
		return categorySumsList
		
		# theToList = []
		# for row in theFromList:
			# theOutLine = row		# filter lower at this point
			# theToList.append(theOutLine)
		# return(theToList)

	def writeListAsCSV(self, outFilePtr, listToWriteOut):
		"""Calls the other function which do the write out of the CSV file
	
		:param outFileName: string which has the pathfilename
		:param theOutList: the list to write out
		"""
		myWriteClass = WriteOutToCSVFile()
		outFilePtr = myWriteClass.openCSVFileForWrites(outFileName)			# start at the same folder as the input file was located
		outFilePtr.writerows(listToWriteOut)					# write out the BOM list to the output CSV file
					
	def theExecutive(self):
		global defaultPath
		global outFileName
		
		print 'Loading defaults file'
		defaultClass = HandleDefault()
		defaultClass.checkSetDefaults()

		myCSV = FindCSVFile()
		fileToRead = myCSV.findCSVFileBrowse(defaultPath)
		defaultPath = fileToRead[0:fileToRead.rfind('\\')+1]
		defaultList = []
		defaultItem = []
		defaultItem.append('DEFAULT_PATH')
		defaultItem.append(defaultPath)
		defaultList.append(defaultItem)
		defaultClass.storeDefaults(defaultList)

		outFileName = fileToRead[:-4] + "_Accts.csv"

		try:
			inFile = open(fileToRead, 'rb')
		except IOError:
			errorDialog('ERROR - Cannot open input file')
			exit()
		
		try:
			outFile = open(outFileName, 'w')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(outFileName, 'w')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()

		theInList = self.readInCSVToList(inFile)
		theOutList = self.processList(theInList)
		self.writeListAsCSV(outFile, theOutList)

class UIManager:
	"""The UI manager
	"""
	interface = """
	<ui>
		<menubar name="MenuBar">
			<menu action="File">
				<menuitem action="Open"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="Help">
				<menuitem action="About"/>
			</menu>
		</menubar>
	</ui>
	"""

	def __init__(self):
		"""Initialize the class
		"""
		# Create the top level window
		window = gtk.Window()
		window.connect('destroy', lambda w: gtk.main_quit())
		window.set_default_size(200, 200)
		
		vbox = gtk.VBox()
		
		# Create a UIManager instance
		uimanager = gtk.UIManager()

		# Add the accelerator group to the toplevel window
		accelgroup = uimanager.get_accel_group()
		window.add_accel_group(accelgroup)
		window.set_title('pyPayPal - Tindie Order Processing')

		# Create the base ActionGroup
		actiongroup0 =	gtk.ActionGroup("pyPayPal")
		self.actiongroup0 = actiongroup0

		# Create actions
		self.actiongroup0.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyPayPal", self.about_pyPayPal),
									])
		uimanager.insert_action_group(self.actiongroup0, 0)
		uimanager.add_ui_from_string(self.interface)

		# Create an ActionGroup
		actiongroup = gtk.ActionGroup('UIMergeExampleBase')
		self.actiongroup = actiongroup

		# Add the actiongroup to the uimanager
		uimanager.insert_action_group(actiongroup, 1)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		"""Open the interface by calling the control class
		"""
		myControl = ControlClass()
		myControl.theExecutive()

		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("Conversion Complete")
		message.run()		# Display the dialog box and hang around waiting for the "OK" button
		message.destroy()	# Takes down the dialog box
		return

	def about_pyPayPal(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyPayPal\nAuthor: Doug Gilliland\n(c) 2015 - Doug Gilliland - All rights reserved\npyPayPal - Do stuff with PayPal accounting")
		message.run()
		message.destroy()
		return
		
	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
