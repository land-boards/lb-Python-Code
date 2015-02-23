"""
kickMail.py
Reads in the Kickstarter backer file.
Writes out a USPS csv file.
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

shippingNameColumn = 99
address1Column = 99
address2Column = 99
cityColumn = 99
stateColumn = 99
countryColumn = 99
zipColumn = 99
emailColumn = 99
shippingAmtColumn = 99
rewardMinimumColumn = 99
pledgeAmountColumn = 99
rewardsSentColumn = 99
surveyResponseColumn = 99

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
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
		dialog.destroy()
		
class ControlClass:
	"""
	"""
	def readInCSV(self, inFile):
		"""
		"""
		csvReader = csv.reader(inFile)
		list2Read = []
		for row in csvReader:
			list2Read.append(row)
		return list2Read
		
	def mapInputList(self, theInList):
		"""
		Latest input format -
			Backer Number,
			Backer UID,
			Backer Name,
			Email,
			Shipping Country,
			Shipping Amount,
			Reward Minimum,
			Pledge Amount,
			Pledged At,
			Rewards Sent?,
			Pledged Status,
			Notes,
			Survey Response,
			Shipping Name,
			Shipping Address 1,
			Shipping Address 2,
			Shipping City,
			Shipping State,
			Shipping Postal Code,
			Shipping Country Name,			
			Shipping Country Code

		"""
		global emailColumn
		global countryColumn
		global shippingAmtColumn
		global rewardMinimumColumn
		global pledgeAmountColumn
		global rewardsSentColumn
		global shippingNameColumn
		global address1Column
		global address2Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global surveyResponseColumn
		myOutList = []
		header = theInList[0]
		headerLen = len(header)
		itemNum = 0
		for item in header:
			if item == 'Email':
				emailColumn = itemNum
			elif item == 'Shipping Country':
				countryColumn = itemNum
			elif item == 'Shipping Amount':
				shippingAmtColumn = itemNum
			elif item == 'Reward Minimum':
				rewardMinimumColumn = itemNum
			elif item == 'Pledge Amount':
				pledgeAmountColumn = itemNum
			elif item == 'Rewards Sent?':
				rewardsSentColumn = itemNum
			elif item == 'Shipping Name':
				shippingNameColumn = itemNum
			elif item == 'Shipping Address 1':
				address1Column = itemNum
			elif item == 'Shipping Address 2':
				address2Column = itemNum
			elif item == 'Shipping City':
				cityColumn = itemNum
			elif item == 'Shipping State':
				stateColumn = itemNum
			elif item == 'Shipping Postal Code':
				zipColumn = itemNum
			elif item == 'Shipping Country Name':
				countryColumn = itemNum
			elif item == 'Survey Response':
				surveyResponseColumn = itemNum
			itemNum += 1
		# print 'header columns', itemNum
		return

	def countBoards(self, theInList):
		"""
			4 - Shipping Amount, $5.00 USD
			5 - Reward Minimum,
			6 - Pledge Amount,
		"""
		global emailColumn
		global countryColumn
		global shippingAmtColumn
		global rewardMinimumColumn
		global pledgeAmountColumn
		global rewardsSentColumn
		global shippingNameColumn
		global address1Column
		global address2Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global surveyResponseColumn
		boardsCount = 0.0
		unshippedBoardsCount = 0.0
		shippingTotal = 0.0
		rewardTotal = 0.0
		pledgeTotal = 0.0
		backers = 0
		for row in theInList[1:]:
			num = 0.0
			shippingString = row[shippingAmtColumn][1:-4]
			rewardString = row[rewardMinimumColumn][1:-4]
			pledgeString = row[pledgeAmountColumn][1:-4]
			# print shippingString, rewardString, pledgeString
			shippingNum = float(shippingString)
			shippingTotal += shippingNum
			rewardNum = float(rewardString)
			rewardTotal += rewardNum
			pledgeNum = float(pledgeString)
			pledgeTotal += pledgeNum
			# print 'boards', (pledgeNum - shippingNum) / rewardNum
			boardsCount += (pledgeNum - shippingNum) / rewardNum
			if row[rewardsSentColumn] != 'Sent':
				unshippedBoardsCount += (pledgeNum - shippingNum) / rewardNum
			backers += 1
#		print 'Total Rewards =', boardsCount
		outStr = 'Backers = '
		outStr += str(backers)
		outStr += '\nTotal Rewards = '
		outStr += str(boardsCount)
		outStr += '\nUnshipped Rewards = '
		outStr += str(unshippedBoardsCount)
		outStr += '\nTotal Shipping = '
		outStr += str(shippingTotal)
		outStr += '\nTotal Rewards = '
		outStr += str(rewardTotal)
		outStr += '\nTotal Pledges = '
		outStr += str(pledgeTotal)
		outStr += '\nAvg $ per board = $'
		outStr += str(rewardTotal/boardsCount)
		errorDialog(outStr)
	
	def writeOutUSPSAddressBook(self, outFilePtr, theList):
		"""
		Output list -
			0 - First Name,
			1 - MI,
			2 - Last Name,
			3 - Company,
			4 - Address 1,
			5 - Address 2,
			6 - Address 3,
			7 - City,
			8 - State/Province,
			9 - ZIP/Postal Code,
			10 - Country,
			11 - Urbanization (relates to Puerto Rico)
			12 - Phone Number,
			13 - Fax Number,
			14 - E Mail,
			15 - Reference Number,
			16 - Nickname,,,
		First Name,MI,Last Name,Company,Address 1,Address 2,Address 3,City,State/Province,ZIP/Postal Code,Country,Urbanization,Phone Number,Fax Number,E Mail,Reference Number,Nickname
		"""
		global emailColumn
		global countryColumn
		global shippingAmtColumn
		global rewardMinimumColumn
		global pledgeAmountColumn
		global rewardsSentColumn
		global shippingNameColumn
		global address1Column
		global address2Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global surveyResponseColumn
		outFilePtr.writerow(['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname'])
		for row in theList[1:]:
			if (row[rewardsSentColumn] == '') and (row[address1Column] != ''):
				outLine = []
				outLine.append(row[shippingNameColumn])
				outLine.append('')
				outLine.append('')
				outLine.append('')
				outLine.append(row[address1Column])
				outLine.append(row[address2Column])
				outLine.append('')
				outLine.append(row[cityColumn])
				outLine.append(row[stateColumn])
				outLine.append(row[zipColumn])
				outLine.append(row[countryColumn])
				outLine.append('')
				outLine.append('')
				outLine.append('')
				outLine.append(row[emailColumn])
				outFilePtr.writerow(outLine)

	def theExecutive(self):
		"""
		"""
		myCSV = FindCSVFile()
		fileToRead = myCSV.findCSVFileBrowse('.')

		fileToWrite = fileToRead[:-4] + "_USPS.csv"

		try:
			inFile = open(fileToRead, 'rb')
		except IOError:
			errorDialog('ERROR - Cannot open input file')
			exit()
		
		try:
			outCSVFile = csv.writer(open(fileToWrite, 'wb'), delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open in EXCEL?\nClose the file and return.')
			try:
				outCSVFile = csv.writer(open(fileToWrite, 'wb'), delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open in EXCEL?')
				exit()

		theInList = self.readInCSV(inFile)
		self.mapInputList(theInList)
		self.countBoards(theInList)
		self.writeOutUSPSAddressBook(outCSVFile, theInList)

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
		window.set_title('kickMail - Kickkstarter rewards processing program')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("kickMail")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About kickMail", self.about_kickMail),
									])
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
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
		message.set_markup("Processing Complete")
		message.run()		# Display the dialog box and hang around waiting for the "OK" button
		message.destroy()	# Takes down the dialog box
		return

	def about_kickMail(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About kickMail\nAuthor: Doug Gilliland\n(c) 2014 - AAC - All rights reserved\nkickMail Process Deltek T and E Charge Account Report")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
