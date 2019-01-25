"""
pyLbInv.py - Land Boards, LLC Inventory Management Software.

--------
Features
--------

* Uses MySQL to manage inventory.

-----
Setup
-----

TBD

-----
Usage
-----

-----------------
Tindie Input File
-----------------

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
import os
import sys
import mysql.connector

import time
from datetime import date

sys.path.append('C:\\Users\\Doug\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')

from dgProgDefaults import *
from dgReadCSVtoList import *
from dgWriteListtoCSV import *
defaultPath = '.'

# From Tindie
shippingFirstNameColumn = 99
shippingLastNameColumn = 99
address1Column = 99
cityColumn = 99
stateColumn = 99
countryColumn = 99
zipColumn = 99
emailColumn = 99
rewardsSentColumn = 99

def errorDialog(errorString):
	"""
	:param errorDialog: The error message to print
	
	Prints an error message as a dialog box.

	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box

class ControlClass:
	"""Methods to read Tindie file.
	Tindie file has board sales history
	"""
	def theExecutive(self):
		"""The code that calls the other code
		"""
		global defaultPath
		defaultParmsClass = HandleDefault()
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		# print 'defaultPath',defaultPath
		myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
		myCSVFileReadClass.setVerboseMode(False)	# turn on verbose mode until all is working 
		myCSVFileReadClass.setUseSnifferFlag(True)
		theInList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select CSV File')	# read in CSV into list
		if theInList == []:
			doneReading = True
			print 'stuff'
			input()
			exit()
		print 'list is lines', len(theInList)
		print 'theExecutive: theInList', theInList
		#print 'first row of list is', theInList[0]
		#print 'second row of list is', theInList[1]
		self.mapTindieInList(theInList[0])
		outMessage = 'Tindie Statistics\n'
		outMessage += 'Unfiltered list lines : '
		outMessage += str(len(theInList))
		errorDialog(outMessage)
		inFileNameTindie = myCSVFileReadClass.getLastPathFileName()
		renFileNameTindie = inFileNameTindie[0:-4] + "-Tindie-" + str(date.today()) + '.tsv'
		#print 'changing file name from: ', inFileNameTindie, ' to: ', renFileNameTindie
		# os.rename(inFileNameTindie, renFileNameTindie)
		defaultPath = myCSVFileReadClass.getLastPath()
		defaultParmsClass.storeKeyValuePair('DEFAULT_PATH',defaultPath)
		dateToAppend = str(date.today())


print(mydb)

	def mapTindieInList(self, header):
		"""
		:param header: The list header.
		:return: a mapping file with the columns mapped to a column number.
		
		Map the column headers to an internal preferred ordering.
		Latest input format -
		* Order ID
		* Date
		* First Name
		* Last Name
		* Email
		* Street
		* City
		* State / Province
		* Postal/Zip Code
		* Country
		* Additional Instructions
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
		#print header
		myOutList = []
		itemNum = 0
		#print 'mapTindieInList: header',header
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
				#print 'shipped column mapped'
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
		return

	#mydb = mysql.connector.connect(host="localhost",user="yourusername",passwd="yourpassword")

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
		message.set_markup("About TindieMail\nAuthor: Doug Gilliland\n(c) 2015 - land-boards.com - All rights reserved\nTindieMail - Process Timdie orders.cav.\nCreates USPS and PayPal mail order list.")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		"""quit
		"""
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
