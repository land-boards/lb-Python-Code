"""
TindieMail.py - Automate Tindie shipping lists.

--------
Features
--------

* Input is the csv file as exported from Tindie 
* Program provides input field flexibility to allow for some column moving
* Output is a USPS formated CSV file which can be directly imported into the USPS as an Address Book.

----------
Input File
----------

How to export the file from Tindie

* Tindie
* Menu
* My Store
* Export CSV

----
Code
----

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

sys.path.append('C:\\Users\\doug_000\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')

from dgProgDefaults import *
from dgReadCSVtoList import *
from dgWriteListtoCSV import *

shippingFirstNameColumn = 99
shippingLastNameColumn = 99
address1Column = 99
cityColumn = 99
stateColumn = 99
countryColumn = 99
zipColumn = 99
emailColumn = 99
rewardsSentColumn = 99
defaultPath = '.'

def errorDialog(errorString):
	"""Prints an error message as a dialog box.

	:param errorDialog: The error message to print
	
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box

class ControlClass:
	"""Methods to read tindie file and write out USPS and PayPal lists.
	"""
	def theExecutive(self):
		"""The code that calls the other code
		"""
		global defaultPath
		
		defaultParmsClass = HandleDefault()
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		print 'defaultPath',defaultPath

		myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
		myCSVFileReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		theInList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select CSV File')	# read in CSV into list
		if theInList == []:
			return False
		self.mapInputList(theInList)
		uspsList = self.createUSPSAddressList(theInList)
		payPalList = self.createPayPalAddressList(theInList)

		outMessage = 'TindieMail Statistics\n'
		outMessage += 'Unfiltered list lines : '
		outMessage += str(len(theInList))
		outMessage += '\nUSPS list lines : '
		outMessage += str(len(uspsList))
		outMessage += '\nPayPal list lines : '
		outMessage += str(len(payPalList))
		errorDialog(outMessage)

		defaultPath = myCSVFileReadClass.getLastPath()
		defaultParmsClass.storeKeyValuePair('DEFAULT_PATH',defaultPath)

		fileToWriteUSPS = defaultPath + "orders_USPS.csv"
		fileToWritePayPal = defaultPath + "orders_PayPal.csv"

		outFileClass = WriteListtoCSV()
		outFileClass.appendOutFileName('.csv')
		if uspsList != []:
			uspsHeader = ['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname']
			outFileClass.writeOutList(fileToWriteUSPS, uspsHeader, uspsList)
		if payPalList != []:
			payPalHeader = ['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname']
			outFileClass.writeOutList(fileToWritePayPal, payPalHeader, payPalList)
		
	def mapInputList(self, theInList):
		"""Map the column headers to an internal preferred ordering.
		Latest input format -
		* ID
		* Date
		* First Name
		* Last Name
		* Street
		* City
		* State / Province
		* Postal/Zip Code
		* Country
		* Additional Instructions
		* Email
		* Phone	
		* Refunded
		* Shipped
		* Pay Out Status
		* Paid Out
		* Shipping
		* Shipping Amount 
		* Tracking Number
		* Tindie Fee
		* Processing Fee
		* Product Name
		* Option Summary
		* Status
		* Quantity
		* Unit Price
		* Total Price
		* Model Number

		:param theInList: The entire input list.
		:return: a mapping file with the columns mapped to a column number.

		"""
		global emailColumn
		global shippingFirstNameColumn
		global shippingLastNameColumn
		global address1Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global rewardsSentColumn
		myOutList = []
		header = theInList[0]
		headerLen = len(header)
		itemNum = 0
		for item in header:
			if item == 'Email':
				emailColumn = itemNum
			elif item == 'First Name':
				shippingFirstNameColumn = itemNum
			elif item == 'Last Name':
				shippingLastNameColumn = itemNum
			elif item == 'Country':
				countryColumn = itemNum
			elif item == 'Shipped':
				rewardsSentColumn = itemNum
			elif item == 'Shipping Name':
				shippingNameColumn = itemNum
			elif item == 'Street':
				address1Column = itemNum
			elif item == 'Shipping Address 2':
				address2Column = itemNum
			elif item == 'City':
				cityColumn = itemNum
			elif item == 'State / Province':
				stateColumn = itemNum
			elif item == 'Postal/Zip Code':
				zipColumn = itemNum
			#else:
				#print 'unknown/unused header',item
			itemNum += 1
		# print 'header columns', itemNum
		return

	def createUSPSAddressList(self, theList):
		"""Write out the USPS Address book values.
		The output file is a CSV that can be read by the USPS Address Book Import.
		
		Output list -
		
		* 0 - First Name,
		* 1 - MI,
		* 2 - Last Name,
		* 3 - Company,
		* 4 - Address 1,
		* 5 - Address 2,
		* 6 - Address 3,
		* 7 - City,
		* 8 - State/Province,
		* 9 - ZIP/Postal Code,
		* 10 - Country,
		* 11 - Urbanization (relates to Puerto Rico)
		* 12 - Phone Number,
		* 13 - Fax Number,
		* 14 - E Mail,
		* 15 - Reference Number,
		* 16 - Nickname,,,
		
		:param outFilePtr: points to the output file
		:return: no return value
		"""
		global emailColumn
		global shippingFirstNameColumn
		global shippingLastNameColumn
		global address1Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global rewardsSentColumn
		outList = []
		for row in theList[1:]:
			if (row[rewardsSentColumn] == 'False') and (row[countryColumn] != 'United States'):
				outLine = []
				outLine.append(row[shippingFirstNameColumn])
				outLine.append('')
				outLine.append(row[shippingLastNameColumn])
				outLine.append('')
				outLine.append(row[address1Column])
				outLine.append('')
				outLine.append('')
				outLine.append(row[cityColumn])
				outLine.append(row[stateColumn])
				outLine.append(row[zipColumn])
				if row[countryColumn] == 'United Kingdom':
					outLine.append('GREAT BRITAIN AND NORTHERN IRELAND')
				else:
					outLine.append(row[countryColumn])
				outLine.append('')
				outLine.append('')
				outLine.append('')
				outLine.append(row[emailColumn])
				outList.append(outLine)
		return outList

	def createPayPalAddressList(self, theList):
		"""Write out the USPS Address book values.
		The output file is a CSV that can be read by the USPS Address Book Import.
		
		Output list -
		
		* 0 - First Name,
		* 1 - MI,
		* 2 - Last Name,
		* 3 - Company,
		* 4 - Address 1,
		* 5 - Address 2,
		* 6 - Address 3,
		* 7 - City,
		* 8 - State/Province,
		* 9 - ZIP/Postal Code,
		* 10 - Country,
		* 11 - Urbanization (relates to Puerto Rico)
		* 12 - Phone Number,
		* 13 - Fax Number,
		* 14 - E Mail,
		* 15 - Reference Number,
		* 16 - Nickname,,,
		
		:param outFilePtr: points to the output file
		:return: no return value
		"""
		global emailColumn
		global shippingFirstNameColumn
		global shippingLastNameColumn
		global address1Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global rewardsSentColumn
		outList = []
		for row in theList[1:]:
			if (row[rewardsSentColumn] == 'False') and (row[countryColumn] == 'United States'):
			#print 'country', row[countryColumn]
				outLine = []
				outLine.append(row[shippingFirstNameColumn])
				outLine.append('')
				outLine.append(row[shippingLastNameColumn])
				outLine.append('')
				outLine.append(row[address1Column])
				outLine.append('')
				outLine.append('')
				outLine.append(row[cityColumn])
				outLine.append(row[stateColumn])
				outLine.append(row[zipColumn])
				outLine.append(row[countryColumn])
				outLine.append('')
				outLine.append('')
				outLine.append('')
				outLine.append(row[emailColumn])
				outList.append(outLine)
		return outList


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
		window.set_title('TindieMail - Kickkstarter rewards processing program')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("TindieMail")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About TindieMail", self.about_TindieMail),
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

	def about_TindieMail(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About TindieMail\nAuthor: Doug Gilliland\n(c) 2015 - land-boards.com - All rights reserved\nTindieMail - Process Kickstarter Backer Reports")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
