"""
pyTindieList.py
Convert a Tindie CSV order export file into a simple shipping list.
Only gets the records which have not been marked as Shipped and have entered an address.
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

clickAddrLab = False
clickInvPulls = False
clickShipLists = False
checkTheBacklog = False

pathToFile = '.'

def errorDialog(errorString):
	"""
	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return
			
class FindCSVFile:
	def findCSVFileBrowse(self, startingPath):
		"""findCSVFileBrowse() - This is the dialog which locates the csv files
	
		:returns: path/name of the file that was selected
		"""
		csvFileString = "Select orders.csv file"
		dialog = gtk.FileChooserDialog(csvFileString,
			None,
			gtk.FILE_CHOOSER_ACTION_OPEN,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		if startingPath != '':
			dialog.set_current_folder(startingPath)
		else:
			dialog.set_current_folder('.')
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
	def readInCSV(self, inFile):
		csvReader = csv.reader(inFile)
		list2Read = []
		for row in csvReader:
			list2Read.append(row)
		return list2Read
		
	def processTindieList(self, theTindieList):
		'''Tindie list comes in the format:
		[0]=ID,[1]Date,[2]First Name,[3]Last Name,[4]Street,[5]City,[6]State / Province,[7]Postal/Zip Code,[8]Country,[9]Additional Instructions,
		[10]Email,[11]Phone,[12]Refunded,[13]Shipped,[14]Pay Out Status,[15]Paid Out,[16]Shipping,[17]Shipping Amount,[18]Tracking Number,
		[19]Product Name,[20]Option Summary,[21]Status,[22]Weight,[23]Weight Unit,[24]Quantity,[25]Unit Price,[26]Total Price,[27]Model Number
		
		Output list only contains names which have not yet shipped and is in the format:
		[0]First Name,[1]Last Name,[2]Street,[3]City,[4]State / Province,[5]Postal/Zip Code,[6]Product Name,[7]Option Summary,
		[8]Quantity,[9]Model Number
		'''
		theOutList = []
		for row in theTindieList[1:]:
			if row[13] == 'False' and row[21] == 'billed':			# Not yet shipped but paid for already
				theOutLine = []
				theOutLine.append(row[2])
				theOutLine.append(row[3])
				theOutLine.append(row[4])
				theOutLine.append(row[5])
				theOutLine.append(row[6])
				theOutLine.append(row[7])
				theOutLine.append(row[19])
				theOutLine.append(row[20])
				theOutLine.append(row[24])
				theOutLine.append(row[27])
				theOutList.append(theOutLine)
		return(theOutList)

	def writeOutAdrList(self, outFilePtr, theList):
		''' [0]First Name,[1]Last Name,[2]Street,[3]City,[4]State / Province,[5]Postal/Zip Code,[6]Product Name,[7]Option Summary,
		[8]Quantity,[9]Model Number
		'''
		outFilePtr.write('=======================\n')
		outFilePtr.write('Address Labels\n\n')
		for row in theList:
			outFilePtr.write('  ' + row[0] + ' ' + row[1] + '\n')
			outFilePtr.write('  ' + row[2] + '\n')
			outFilePtr.write('  ' + row[3] + ', ' + row[4] +' ' + row[5] + '\n\n')
			
	def writeOutInvPullList(self, outFilePtr, theList):
		'''
		'''
		outFilePtr.write('=======================\n')
		outFilePtr.write('Pull for Shipment List\n\n')
		uniqueParts = []
		uniqueItems = []
		for rowList in theList:
			inUniqueParts = False
			rowNum = 0
			for rowUnique in uniqueParts:
				if rowUnique[6:8] == rowList[6:8] and rowUnique[9] == rowList[9]:
					inUniqueParts = True
			if inUniqueParts == False:
				uniqueParts.append(rowList)
				uniqueItemsLine = []
				uniqueItemsLine.append(rowList[6])
				uniqueItemsLine.append(rowList[7])
				uniqueItemsLine.append(rowList[9])
				uniqueItems.append(uniqueItemsLine)
			rowNum += 1

		totalParts = []
		for part in uniqueItems:
			partCount = 0
			for orderedPart in theList:
				if part[0:2] == orderedPart[6:8] and part[2] == orderedPart[9]:
					partCount += int(orderedPart[8])
					print 'partCount', partCount
			totalPartLine = part
			totalPartLine.append(str(partCount))
			totalParts.append(totalPartLine)
		for row in totalParts:
			outFilePtr.write('qty:' + row[3] + '\n')
			outFilePtr.write(row[0] + '\n')
			outFilePtr.write(row[1] + '\n')
			outFilePtr.write(row[2] + '\n\n')
			
	def writeOutShipList(self, outFilePtr, theList):
		'''
		'''
		outFilePtr.write('=======================\n')
		outFilePtr.write('Ship List\n\n')
		for row in theList:
			outFilePtr.write(row[0] + ' ' + row[1] + '\n')
			outFilePtr.write('qty:' + row[8] + '\n')
			outFilePtr.write(row[6] + '\n')
			outFilePtr.write(row[7] + '\n')
			outFilePtr.write(row[9] + '\n\n')
		
	def theExecutive(self):
		global clickAddrLab
		global clickShipLists
		global clickInvPulls
		global checkTheBacklog
		global pathToFile

		myCSV = FindCSVFile()
		fileToRead = myCSV.findCSVFileBrowse(pathToFile)
		pathToFile = fileToRead[0:fileToRead.rfind('\\')+1]

		fileToWrite = fileToRead[:-4] + "_adr.txt"

		try:
			inFile = open(fileToRead, 'rb')
		except IOError:
			errorDialog('ERROR - Cannot open input file')
			exit()
		
		try:
			outFile = open(fileToWrite, 'w')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(fileToWrite, 'w')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()

		theInList = self.readInCSV(inFile)
		theOutList = self.processTindieList(theInList)
		if clickAddrLab:
			self.writeOutAdrList(outFile, theOutList)
		if clickShipLists:
			self.writeOutInvPullList(outFile, theOutList)
		if clickInvPulls:
			self.writeOutShipList(outFile, theOutList)
		if checkTheBacklog:
			self.checkTheBacklog(outFile, theInList)

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
			<menu action="Options">
				<menuitem action="Adr_Lab"/>
				<menuitem action="Inv_Pulls"/>
				<menuitem action="Ship_List"/>
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
		window.set_title('pyTindieList - Tindie Order Processing')

		# Create the base ActionGroup
		actiongroup0 =	gtk.ActionGroup("pyTindieList")
		self.actiongroup0 = actiongroup0

		# Create actions
		self.actiongroup0.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Options", None, "_Options"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyTindieList", self.about_pyTindieList),
									])
		uimanager.insert_action_group(self.actiongroup0, 0)
		uimanager.add_ui_from_string(self.interface)

		# Create an ActionGroup
		actiongroup = gtk.ActionGroup('UIMergeExampleBase')
		self.actiongroup = actiongroup

		# Create a ToggleAction, etc.
		actiongroup.add_toggle_actions([("Adr_Lab", gtk.STOCK_PREFERENCES, "_Create Address Labels", None, "", self.clickAddrLab)])
		actiongroup.add_toggle_actions([("Inv_Pulls",gtk.STOCK_PREFERENCES, "_Create Inventory Pull Lists", None, "", self.clickInvPulls)])
		actiongroup.add_toggle_actions([("Ship_List",gtk.STOCK_PREFERENCES, "_Create Shipping Lists", None, "", self.clickShipLists)])

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

	def about_pyTindieList(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyTindieList\nAuthor: Doug Gilliland\n(c) 2014 - Doug Gilliland - All rights reserved\npyTindieList - create an address list for labels from Tindie")
		message.run()
		message.destroy()
		return
		
		

	def clickAddrLab(self, action):
		"""Address Label was clicked
		"""
		global clickAddrLab
		clickAddrLab = not clickAddrLab
		if clickAddrLab == True:
			print 'selected option to print address labels'
		else:
			print 'deselected option to print address labels'
		return
		
	def clickInvPulls(self, action):
		"""Inventory Pulls was clicked
		"""
		global clickInvPulls
		clickInvPulls = not clickInvPulls
		if clickInvPulls == True:
			print 'selected option to print inventory pull list'
		else:
			print 'deselected option to print inventory pull list'
		return
		
	def clickShipLists(self, action):
		"""Ship Lists was clicked
		"""
		global clickShipLists
		clickShipLists = not clickShipLists
		if clickShipLists == True:
			print 'selected option to print shipping pull list'
		else:
			print 'deselected option to print shipping pull list'
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
