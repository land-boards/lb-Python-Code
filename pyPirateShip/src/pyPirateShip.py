"""
pyPirateShip.py - Automate Tindie shipping lists.

--------
Features
--------

* Input is the csv or tsv file(s) as exported from Tindie 
* Intent of this program is to automate a lot of copy-pasting of data for shipping.
* Program provides input field flexibility to allow for some column moving
* There are two possible types of file output
* One of the output formats is PayPal multiple shipping formated CSV file for US shipping
* The other output format is json file (used with bookmarklet.js and the USPS site for foreign shipping)
* Output Files are only produced for items which have not yet shippped.

-----
Setup
-----


-----
Usage
-----

* Run this program one Tindie file is selected.
* Statistics will be shown for Kickstarter rewards (how many rewards, etc).

-----------------
Tindie Input File
-----------------

How to export the file from Tindie

* Tindie
* Store icon
* My Store
* Orders
* Export
* Shipping: Unshipped
* File Typr CSV
* Export
* Save as into folder on PC
* Run this program

-----------------------
PirateShip Import Steps
-----------------------

* Log into PirateShip website
* Select spreadsheet

----
Code
----

"""

import csv
import string
import os
import sys
from sys import version_info
import json

import time
from datetime import date

# Fix path below if imports fail
sys.path.append('C:\\Users\\HPz420\\Documents\\GitHub\\land-boards\\lb-Python-Code\\dgCommonModules\\TKDGCommon')

from dgProgDefaultsTk import *
from dgReadCSVtoListTk import *
from dgWriteListtoCSVTk import *

from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

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

class ControlClass:
	"""Methods to read tindie or Kickstarter files and write out USPS and PayPal lists.
	"""
	def doConvert(self):
		"""The code that calls the other code
		"""
		global defaultPath
		defaultParmsClass = HandleDefault()
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		# print '(doConvert): defaultPath',defaultPath
		myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
		myCSVFileReadClass.setVerboseMode(False)	# turn on verbose mode until all is working 
		myCSVFileReadClass.setUseSnifferFlag(True)
		doneReading = False
		endList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select TSV File')	# read in TSV into list
		if endList == []:
			errorDialog("doConvert): No file selected")
			return
		#print 'doConvert): list is lines', len(endList)
		#print 'doConvert): theExecutive: endList', endList

		#print 'doConvert): first row of list is', endList[0]
		#print 'doConvert): second row of list is', endList[1]
		if self.mapTindieInList(endList[0]) == False:
			errorDialog("doConvert): File mapping error")
			return
		pirateShipListUS = self.createPirateUSAShipAddrList(endList[1:])
		pirateShipListForeign = self.createPirateForeignShipAddrList(endList[1:])
		
		outMessage = '(doConvert): pyPirateShip Statistics\n'
		outMessage += 'List lines : '
		outMessage += str(len(endList)-1)
		outMessage += '\nUS lines : '
		outMessage += str(len(pirateShipListUS))
		outMessage += '\nForeign lines : '
		outMessage += str(len(pirateShipListForeign))
		
		errorDialog(outMessage)
		inFileNameTindie = myCSVFileReadClass.getLastPathFileName()
		renFileNameTindie = inFileNameTindie[0:-4] + "-Tindie-" + str(date.today()) + '.tsv'
		#print '(doConvert): changing file name from: ', inFileNameTindie, ' to: ', renFileNameTindie
		os.rename(inFileNameTindie, renFileNameTindie)
		defaultPath = myCSVFileReadClass.getLastPath()
		defaultParmsClass.storeKeyValuePair('DEFAULT_PATH',defaultPath)
		dateToAppend = str(date.today())

		fileToWritePship = defaultPath + "US_orders_PirateShip-"
		fileToWritePship += dateToAppend
		fileToWritePship += ".csv"

		outFileClass = WriteListtoCSV()
		outFileClass.appendOutFileName('.csv')
		if pirateShipListUS != []:
			#print '(doConvert): len of pirateShipListUS', len(pirateShipListUS)
			pirateShipHeader = ['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname']
			outFileClass.writeOutList(fileToWritePship, pirateShipHeader, pirateShipListUS)

		fileToWritePship = defaultPath + "Foreign_orders_PirateShip-"
		fileToWritePship += dateToAppend
		fileToWritePship += ".csv"

		outFileClass = WriteListtoCSV()
		outFileClass.appendOutFileName('.csv')
		if pirateShipListForeign != []:
			#print '(doConvert): len of pirateShipListForeign', len(pirateShipListForeign)
			pirateShipHeader = ['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname']
			outFileClass.writeOutList(fileToWritePship, pirateShipHeader, pirateShipListForeign)
		
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
		* Company Title
		* Phone	
		* Street
		* City
		* State / Province
		* Postal/Zip Code
		* Country
		* Additional Instructions
		* Shipping Methods
		* Shipping Total
		* Discount Total
		* Discount Codes
		* Tax Total
		* Order Total
		* Tindie Fee
		* Processing Fee
		* Total Payable to Seller
		* Refunded
		* Shipped
		* Tracking Number		
		* Pay Out Status
		* Paid Out
		* Product Name
		* Option Summmary
		* Model Number
		* Status
		* Unit Price
		* Discount Price
		* Quantity
		* Total Item Price

		"""
		global shippingFirstNameColumn
		global shippingLastNameColumn
		global companyColumn
		global address1Column
		global address2Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global phoneNumberColumn
		global emailColumn
		global rewardsSentColumn
		#print header
		myOutList = []
		itemNum = 0
		#print 'mapTindieInList: header',header
		for item in header:
			if item == 'First Name':
				shippingFirstNameColumn = itemNum
			elif item == 'Last Name':
				shippingLastNameColumn = itemNum
			elif item == 'Company Title':
				companyColumn = itemNum
			elif item == 'Street':
				address1Column = itemNum
			elif item == 'City':
				cityColumn = itemNum
			elif item == 'State / Province':
				stateColumn = itemNum
			elif item == 'Postal/Zip Code':
				zipColumn = itemNum
			elif item == 'Country':
				countryColumn = itemNum
			elif item == 'Phone':
				phoneNumberColumn = itemNum
			elif item == 'Email':
				emailColumn = itemNum
			elif item == 'Shipped':
				rewardsSentColumn = itemNum
				#print 'shipped column mapped'
			#else:
				#print 'unknown/unused header',item
			itemNum += 1
		if shippingFirstNameColumn == 99:
			return False
		return True

	def createPirateForeignShipAddrList(self, theList):
		"""
		:param theList: the List
		:return: List
		
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
		
		"""
		global shippingFirstNameColumn
		global shippingLastNameColumn
		global companyColumn
		global address1Column
		global address2Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global phoneNumberColumn
		global emailColumn
		global rewardsSentColumn
		outList = []
		for row in theList:
			if row[rewardsSentColumn] == 'False' and row[countryColumn] != 'United States of America':
			#print 'country', row[countryColumn]
				outLine = []
				outLine.append(row[shippingFirstNameColumn])
				outLine.append('')
				outLine.append(row[shippingLastNameColumn])
				outLine.append(row[companyColumn])
				numAddrLines = row[address1Column].count('\n') + 1
				if numAddrLines == 1:
					firstAddrLine = row[address1Column]
					secondAddrLine = ''
					thirdAddrLine = ''
				elif numAddrLines == 2:
					firstAddrLine = row[address1Column][0:string.find(row[address1Column],'\n')-1]
					offset1 = string.find(row[address1Column],'\n')
					secondAddrLine = row[address1Column][offset1+1:]
					thirdAddrLine = ''
				elif numAddrLines == 3:
					firstAddrLine = row[address1Column][0:string.find(row[address1Column],'\n')-1]
					offset1 = string.find(row[address1Column],'\n')
					offset2 = string.find(row[address1Column][offset1+1:],'\n')
					secondAddrLine = row[address1Column][offset1+1:offset1+offset2]
					thirdAddrLine = row[address1Column][offset1+offset2+2:]
				else:
					errorDialog('Too many address lines')
				outLine.append(firstAddrLine)
				outLine.append(secondAddrLine)
				outLine.append(thirdAddrLine)
				outLine.append(row[cityColumn])
				outLine.append(row[stateColumn])
				outLine.append(row[zipColumn])
				outLine.append(row[countryColumn])
				outLine.append('')		# urbanization code for Puerto Rico
				outLine.append(row[phoneNumberColumn])
				outLine.append('')		# fax
				outLine.append(row[emailColumn])
				outList.append(outLine)
		return outList

	def createPirateUSAShipAddrList(self, theList):
		"""
		:param theList: the List
		:return: List
		
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
		
		"""
		global shippingFirstNameColumn
		global shippingLastNameColumn
		global companyColumn
		global address1Column
		global address2Column
		global cityColumn
		global stateColumn
		global zipColumn
		global countryColumn
		global phoneNumberColumn
		global emailColumn
		global rewardsSentColumn
		outList = []
		for row in theList:
			if row[rewardsSentColumn] == 'False' and row[countryColumn] == 'United States of America':
			#print 'country', row[countryColumn]
				outLine = []
				outLine.append(row[shippingFirstNameColumn])
				outLine.append('')
				outLine.append(row[shippingLastNameColumn])
				outLine.append(row[companyColumn])
				numAddrLines = row[address1Column].count('\n') + 1
				if numAddrLines == 1:
					firstAddrLine = row[address1Column]
					secondAddrLine = ''
					thirdAddrLine = ''
				elif numAddrLines == 2:
					firstAddrLine = row[address1Column][0:string.find(row[address1Column],'\n')-1]
					offset1 = string.find(row[address1Column],'\n')
					secondAddrLine = row[address1Column][offset1+1:]
					thirdAddrLine = ''
				elif numAddrLines == 3:
					firstAddrLine = row[address1Column][0:string.find(row[address1Column],'\n')-1]
					offset1 = string.find(row[address1Column],'\n')
					offset2 = string.find(row[address1Column][offset1+1:],'\n')
					secondAddrLine = row[address1Column][offset1+1:offset1+offset2]
					thirdAddrLine = row[address1Column][offset1+offset2+2:]
				else:
					errorDialog('Too many address lines')
				outLine.append(firstAddrLine)
				outLine.append(secondAddrLine)
				outLine.append(thirdAddrLine)
				outLine.append(row[cityColumn])
				outLine.append(row[stateColumn])
				outLine.append(row[zipColumn])
				outLine.append(row[countryColumn])
				outLine.append('')		# urbanization code for Puerto Rico
				outLine.append(row[phoneNumberColumn])
				outLine.append('')		# fax
				outLine.append(row[emailColumn])
				outList.append(outLine)
		return outList

		
class Dashboard:
	def __init__(self):
		self.win = Tk()
		self.win.geometry("320x240")
		self.win.title("pyPirateShip.py")

	def add_menu(self):
		self.mainmenu = Menu(self.win)
		self.win.config(menu=self.mainmenu)

		self.filemenu = Menu(self.mainmenu, tearoff=0)
		self.mainmenu.add_cascade(label="File",menu=self.filemenu)

		self.filemenu.add_command(label="Open file",command=control.doConvert)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit",command=self.win.quit)

		self.win.mainloop()

if __name__ == "__main__":
	if version_info.major != 3:
		errorDialog("Requires Python 3")
	control = ControlClass()
	x = Dashboard()
	x.add_menu()
