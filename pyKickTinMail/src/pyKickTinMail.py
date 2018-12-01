"""
TindieMail.py - Automate Kickstarter and Tindie shipping lists.

--------
Features
--------

* Input is the csv or tsv file(s) as exported from Kickstarter or Tindie 
* Intent of this program is to automate a lot of copy-pasting of data for shipping.
* Program provides input field flexibility to allow for some column moving
* There are two possible types of file output
* One of the output formats is PayPal multiple shipping formated CSV file for US shipping
* The other output format is json file (used with bookmarklet.js and the USPS site for foreign shipping)
* Output Files are only produced for items which have not yet shippped.

-----
Setup
-----

* For the USPS (Foreign shipment) output - 
* Create a bookmark in Firefox and put the bookmarklet.js script into the bookmark.
* Properties, location, paste javascript:(funct...
* Name as KickerMailScript

-----
Usage
-----

* Run this program selecting as many input files as you wish.
* Typically only one Tindie file is selected.
* More than one Kickstarter file can be selected.
* Statistics will be shown for Kickstarter rewards (how many rewards, etc).
* The PayPal file is loaded from inside PayPal Multi-Order Shipping.
* The USPS file is run by copy-pasting one line at a time from the .json output.
* Select the bookmark (setup in the Setup above) and do the copy-paste.
* Being in wordwrap on NotePad++ helps for copy.

-----------------
Tindie Input File
-----------------

How to export the file from Tindie

* Tindie
* Menu
* My Store
* Export CSV

----------------------
Kickstarter Input File
----------------------

How to export the file from Kickstarter

* Kickstarter
* Menu (on)
* Backer Report
* Export
* All Reward Tiers
* Save to ZIP
* Extract into CSV file(s)
* This program can combine separate files/rewards

-------------------
PayPal Import Steps
-------------------

* Log into PayPal
* Under Selling Tools
* Select MultiOrder Shipping
* Select Import From file: Import
* Select from a file radio button
* Browse and Select the File name to import
* Click Import
* Setup mapping and make sure to save the mapping 
* If already set up, select this mapping
* Select Done
* Fix any errors and retry
* Select Finished
* You can select multiple rows and set them to use the same weight/service type

-----------------
USPS Import Steps
-----------------

* Log into USPS website
* Select Mail & Ship: Print & Ship
* Should be in Create Label
* Open the json program created by this program into NotePad++ (or equivalent)
* Select KickerMailScript button on Bookmarks bar
* Copy/paste a line from NotePad++
* That will fill in most if not all of the page with default values
* Shipping method, weight, etc can vary so verify that the defaults are OK
* Select a service type
* Select Continue to go to the next screen
* Select the KickerMailScript button
* This time the script will autofill the screen based on defaults
* Verify the defaults are correct
* Select Continue to go to the next screen
* If there are more labels, select Create Another Label
* Rinse and repeat for all labels

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
import json

import time
from datetime import date

#sys.path.append('C:\\Users\\doug_000\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')
#sys.path.append('C:\\Users\\DGilliland\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')
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

# From Kickstarter
shippingNameColumn = 99
address2Column = 99
shippingAmtColumn = 99
rewardMinimumColumn = 99
pledgeAmountColumn = 99
surveyResponseColumn = 99

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
	"""Methods to read tindie or Kickstarter files and write out USPS and PayPal lists.
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
		doneReading = False
		firstLine = []
		accumList = []
		endList = []
		while not doneReading:		# if the list is a Kickstarter list then keep reading until cancel
			theInList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select CSV File')	# read in CSV into list
			if theInList == []:
				doneReading = True
				break
			inFileType = self.determineInputFileType(theInList[0])
			if inFileType == 2:			# Tindie list type only goes through once
				doneReading = True
				accumList = theInList
				break
			else:
				firstLine = theInList[0]
				for row in theInList[1:]:
					accumList.append(row)
		if inFileType == 1:
			endList.append(firstLine)
			endList += accumList
		elif inFileType == 2:
			endList = firstLine
			for row in accumList:
				endList.append(row)
		#print 'list is lines', len(endList)
		#print 'theExecutive: endList', endList

		if inFileType == 1:		# Kickstarter
			self.mapKickInList(endList[0])
			self.countKickBoards(endList[1:])
			uspsList = self.createKickUSPSAddrList(endList[1:])
			payPalList = self.createKickPayPalAddrList(endList[1:])
		elif inFileType == 2:	# Tindie
			#print 'first row of list is', endList[0]
			#print 'second row of list is', endList[1]
			self.mapTindieInList(endList[0])
			uspsList = self.createTindieUSPSAddrList(endList[1:])
			payPalList = self.createTindiePayPayAddrList(endList[1:])
			outMessage = 'TindieMail Statistics\n'
			outMessage += 'Unfiltered list lines : '
			outMessage += str(len(endList))
			outMessage += '\nUSPS list lines : '
			outMessage += str(len(uspsList))
			outMessage += '\nPayPal list lines : '
			outMessage += str(len(payPalList))
			errorDialog(outMessage)
			inFileNameTindie = myCSVFileReadClass.getLastPathFileName()
			renFileNameTindie = inFileNameTindie[0:-4] + "-Tindie-" + str(date.today()) + '.tsv'
			#print 'changing file name from: ', inFileNameTindie, ' to: ', renFileNameTindie
			os.rename(inFileNameTindie, renFileNameTindie)
		else:
			errorDialog('Could not determine input file type')
			exit()
		defaultPath = myCSVFileReadClass.getLastPath()
		defaultParmsClass.storeKeyValuePair('DEFAULT_PATH',defaultPath)
		dateToAppend = str(date.today())

		fileToWriteUSPS = defaultPath + "orders_USPS-"
		fileToWriteUSPS += dateToAppend
		fileToWriteUSPS += ".csv"
		fileToWritePayPal = defaultPath + "orders_PayPal-"
		fileToWritePayPal += dateToAppend
		fileToWritePayPal += ".csv"
		fileToWriteJSON = defaultPath + "orders_USPS-"
		fileToWriteJSON += dateToAppend
		fileToWriteJSON += ".json"

		outFileClass = WriteListtoCSV()
		outFileClass.appendOutFileName('.csv')
		if uspsList != []:
			uspsHeader = ['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname']
			# outFileClass.writeOutList(fileToWriteUSPS, uspsHeader, uspsList)
			self.writeOutJSON(fileToWriteJSON, uspsHeader, uspsList)
		if payPalList != []:
			#print 'len of payPalList', len(payPalList)
			payPalHeader = ['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname']
			outFileClass.writeOutList(fileToWritePayPal, payPalHeader, payPalList)

	def writeOutJSON(self, fileNameJSON, header, data):
		"""
		
		:param fileNameJSON: 
		:param header: 
		:param data: 
		:return: json_lines

		"""
		objects = self.flat_to_objects(header, data)
		json_lines = '\n\n'.join(json.dumps(obj) for obj in objects)
		with open(fileNameJSON, 'w') as f:
			f.write(json_lines)

	def flat_to_objects(self, js_like_header, data):
		"""
		
		:param js_like_header: 
		:param data: 
		:return: objects

		"""
		return map(lambda row: self.row_to_dict(js_like_header, row), data)

	def row_to_dict(self, js_like_header, row):
		"""
		
		:param js_like_header: 
		:param row: 
		:return: dict

		"""
		result = {}
		for (heading, data) in zip(js_like_header, row):
			result[heading] = data
		return result

	def mapKickInList(self, header):
		"""
		:param header: The list header.
		:return: Nothing
		
		Map the column headers to an internal preferred ordering.
		Latest input format -
		
		* Backer Number,
		* Backer UID,
		* Backer Name,
		* Email,
		* Shipping Country,
		* Shipping Amount,
		* Reward Minimum,
		* Pledge Amount,
		* Pledged At,
		* Rewards Sent?,
		* Pledged Status,
		* Notes,
		* Survey Response,
		* Shipping Name,
		* Shipping Address 1,
		* Shipping Address 2,
		* Shipping City,
		* Shipping State,
		* Shipping Postal Code,
		* Shipping Country Name,			
		* Shipping Country Code
		
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
		itemNum = 0
		for item in header:
			if item == 'Email':
				emailColumn = itemNum
			elif item == 'Shipping Country':
				countryColumn = itemNum
			elif item == 'Shipping Amount':
				shippingAmtColumn = itemNum
				print 'shippingAmtColumn',shippingAmtColumn
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

	def countKickBoards(self, theInList):
		"""			
		:param theInList: The entire list
		:return: no value
		
		Count the boards and generate a snapshot of the data.
		
		* 4 - Shipping Amount, $5.00 USD
		* 5 - Reward Minimum,
		* 6 - Pledge Amount,
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
		unshippedBackers = 0
		shippingNum = 0.0
		#print 'countKickBoards: theInList',theInList
		for row in theInList:
			num = 0.0
			# print 'countKickBoards: row',row
			shippingString = row[shippingAmtColumn][1:]
			rewardString = row[rewardMinimumColumn][1:]
			pledgeString = row[pledgeAmountColumn][1:]
#			print 'shippingAmtColumn',shippingAmtColumn
#			print 'row[shippingAmtColumn]',row[shippingAmtColumn]
#			print 'shippingString',shippingString
			shippingNum = float(shippingString)
			shippingTotal += shippingNum
			rewardNum = float(rewardString)
			rewardTotal += rewardNum
			pledgeNum = float(pledgeString)
			pledgeTotal += pledgeNum
			# print 'countKickBoards: boards', (pledgeNum - shippingNum) / rewardNum
			boardsCount += (pledgeNum - shippingNum) / rewardNum
			# print shippingString, rewardString, pledgeString, (pledgeNum - shippingNum) / rewardNum
			if row[rewardsSentColumn] != 'Sent':
				unshippedBoardsCount += (pledgeNum - shippingNum) / rewardNum
				unshippedBackers += 1
			backers += 1
		outStr = 'Total Backers = '
		outStr += str(backers)
		outStr += '\nTotal Rewards = '
		outStr += '{0:.2f}'.format(boardsCount)
		outStr += '\n-\nUnshipped Backers = '
		outStr += str(unshippedBackers)
		outStr += '\nUnshipped Boards = '
		outStr += str(unshippedBoardsCount)
		outStr += '\n-\nTotal Shipping = $'
		outStr += '{0:.2f}'.format(shippingTotal)
		outStr += '\nTotal Pledges = $'
		outStr += '{0:.2f}'.format(pledgeTotal)
		outStr += '\nAvg $ per board = $'
		outStr += '{0:.2f}'.format((pledgeTotal-shippingTotal)/boardsCount)
		errorDialog(outStr)
	
	def createKickUSPSAddrList(self, theList):
		"""
		:param theList: list
		:return: list
		
		Write out the USPS Address book values.
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
		global surveyResponseColumn
		if address1Column == 99:
			errorDialog("Not yet funded")
			return []
		outList = []
		for row in theList:
			if len(row) > 12:
				if (row[rewardsSentColumn] == '') and (row[address1Column] != '') and (row[countryColumn] != 'United States'):
					outLine = []
					firstName = row[shippingNameColumn][0:row[shippingNameColumn].find(' ')]
					lastName = row[shippingNameColumn][row[shippingNameColumn].rfind(' ')+1:]
					if row[shippingNameColumn].find(' ') < row[shippingNameColumn].rfind(' '):
						middleInit = row[shippingNameColumn][row[shippingNameColumn].find(' '):row[shippingNameColumn].find(' ')+2]
					else:
						middleInit = ''
					outLine.append(firstName)
					outLine.append(middleInit)
					outLine.append(lastName)
					outLine.append('')
					outLine.append(row[address1Column])
					outLine.append(row[address2Column])
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

	def createKickPayPalAddrList(self, theList):
		"""
		:param theList: the List
		:return: List
		
		Write out the USPS Address book values.
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
		global surveyResponseColumn
		if address1Column == 99:
			return []
		outLine = []
		outList = []
		for row in theList:
			if len(row) > 12:
				# print 'country', row[countryColumn]
				if (row[rewardsSentColumn] == '') and (row[address1Column] != '') and (row[countryColumn] == 'United States'):
					outLine = []
					firstName = row[shippingNameColumn][0:row[shippingNameColumn].find(' ')]
					lastName = row[shippingNameColumn][row[shippingNameColumn].rfind(' ')+1:]
					if row[shippingNameColumn].find(' ') < row[shippingNameColumn].rfind(' '):
						middleInit = row[shippingNameColumn][row[shippingNameColumn].find(' '):row[shippingNameColumn].find(' ')+2]
					else:
						middleInit = ''
					outLine.append(firstName)
					outLine.append(middleInit)
					outLine.append(lastName)
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
					outList.append(outLine)
		return outList
					
	def determineInputFileType(self, theInList):
		"""
		:params theInList: in file list
		
		Look at the top row of the file to determine the input file type.
		
		"""
		if theInList[0] == 'Backer Id':	# Kickstarter
			return 1
		elif theInList[0] == 'Backer Number':	# Kickstarter
			return 1
		elif theInList[0] == '\xef\xbb\xbfBacker Number' and theInList[1] == 'Backer UID':	# Kickstarter
			return 1
		elif theInList[0] == '\xef\xbb\xbfID' or theInList[0] == 'ID':		# Tindie
			return 2
		elif theInList[0] == '\xef\xbb\xbfOrder ID' or theInList[0] == 'Order ID':		# Tindie
			return 2
		else:
			print 'first line', theInList
			errorDialog('determineInputFileType: Unable to detect the input file format\nExiting')
			exit()
	
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

	def createTindieUSPSAddrList(self, theList):
		"""
		:param theList: the List
		:return: List
		
		Write out the USPS Address book values.
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
		for entryInRow in theList:
			#print entryInRow
			#print 'rewardsSentColumn',rewardsSentColumn
			#print 'countryColumn',countryColumn
			#print '',
			if entryInRow == []:
				break
			if ((entryInRow[rewardsSentColumn] == 'False') or (entryInRow[rewardsSentColumn] == 'FALSE')) and (entryInRow[countryColumn] != 'United States of America'):
				outLine = []
				outLine.append(entryInRow[shippingFirstNameColumn])
				outLine.append('')
				outLine.append(entryInRow[shippingLastNameColumn])
				outLine.append('')
				numAddrLines = string.count(entryInRow[address1Column],'\n') + 1
				if numAddrLines == 1:
					firstAddrLine = entryInRow[address1Column]
					secondAddrLine = ''
					thirdAddrLine = ''
				elif numAddrLines == 2:
					firstAddrLine = entryInRow[address1Column][0:string.find(entryInRow[address1Column],'\n')-1]
					offset1 = string.find(entryInRow[address1Column],'\n')
					secondAddrLine = entryInRow[address1Column][offset1+1:]
					thirdAddrLine = ''
				elif numAddrLines == 3:
					firstAddrLine = entryInRow[address1Column][0:string.find(entryInRow[address1Column],'\n')-1]
					offset1 = string.find(entryInRow[address1Column],'\n')
					offset2 = string.find(entryInRow[address1Column][offset1+1:],'\n')
					secondAddrLine = entryInRow[address1Column][offset1+1:offset1+offset2]
					thirdAddrLine = entryInRow[address1Column][offset1+offset2+2:]
				else:
					errorDialog('Too many address lines')
				outLine.append(firstAddrLine)
				outLine.append(secondAddrLine)
				outLine.append(thirdAddrLine)
				outLine.append(entryInRow[cityColumn])
				outLine.append(entryInRow[stateColumn])
				outLine.append(entryInRow[zipColumn])
				if entryInRow[countryColumn] == 'United Kingdom':
					outLine.append('GREAT BRITAIN AND NORTHERN IRELAND')
				else:
					outLine.append(entryInRow[countryColumn])
				outLine.append('')
				outLine.append('')
				outLine.append('')
				outLine.append(entryInRow[emailColumn])
				outList.append(outLine)
		return outList

	def createTindiePayPayAddrList(self, theList):
		"""
		:param theList: the List
		:return: List
		
		Write out the USPS Address book values.
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
		for row in theList:
			if ((row[rewardsSentColumn] == 'False') or (row[rewardsSentColumn] == 'FALSE')) and (row[countryColumn] == 'United States of America'):
			#print 'country', row[countryColumn]
				outLine = []
				outLine.append(row[shippingFirstNameColumn])
				outLine.append('')
				outLine.append(row[shippingLastNameColumn])
				outLine.append('')
				numAddrLines = string.count(row[address1Column],'\n') + 1
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
