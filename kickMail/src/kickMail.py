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
		
	def surveySent(self, theInList):
		"""
		If the survey has not been sent, the header has 
			Backer Id,Backer Name,Email,Shipping Country,Shipping Amount,Reward Minimum,Pledge Amount,Pledged At,Rewards Sent?,Pledged Status,Notes
		"""
		if len(theInList[0]) > 12:
			print 'Survey has been sent'
			return True
		print 'Survey has not yet been sent'
		return False
		
	def processList(self, theInList):
		"""
		Re-order the list.
		Input list -
			0 - Backer Id,
			1 - Backer Name,
			2 - Email,
			3 - Shipping Country (Two letter code)
			4 - Shipping Amount,
			5 - Reward Minimum,
			6 - Pledge Amount,
			7 - Pledged At,
			8 - Rewards Sent? ('Sent' or blank) 
			9 - Pledged Status ('collected')
			10 - Notes,
			11 - Survey Response,
			12 - Shipping Name,
			13 - Shipping Address 1,
			14 - Shipping Address 2,
			15 - Shipping City,
			16 - Shipping State,
			17 - Shipping Postal Code,
			18 - Shipping Country Name (spelled out name)
			19 - Shipping Country Code (same as 3)
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
		"""
		myOutList = []
		for row in theInList[1:]:
			if row[11] != '' and row[8] != 'Sent' and row[9] == 'collected':
				outRow = []
				outRow.append(row[12][0:row[12].find(' ')])		# 0 - first name
				outRow.append('')								# 1 - Middle initial
				outRow.append(row[12][row[12].find(' ')+1:])	# 2 - last name
				outRow.append('')			# 3 - company
				outRow.append(row[13])		# 4 - address1
				outRow.append(row[14])		# 5 - address2
				outRow.append('')			# 6 - address3
				outRow.append(row[15])		# 7 - city
				outRow.append(row[16])		# 8 - state
				outRow.append(row[17])		# 9 - ZIP code
				outRow.append(row[19])		# 10 - country
				outRow.append('')			# 11 - Urbanization
				outRow.append('')			# 12 - Phone Number
				outRow.append('')			# 13 - fax number
				outRow.append(row[2])		# 14 - email
				outRow.append('')			# 15 - Nickname
				myOutList.append(outRow)
		return myOutList

	def countBoards(self, theInList):
		"""
			4 - Shipping Amount, $5.00 USD
			5 - Reward Minimum,
			6 - Pledge Amount,
		"""
		boardsCount = 0.0
		shippingTotal = 0.0
		rewardTotal = 0.0
		pledgeTotal = 0.0
		backers = 0
		for row in theInList[1:]:
			num = 0.0
			shippingString = row[4][1:-4]
			rewardString = row[5][1:-4]
			pledgeString = row[6][1:-4]
			# print shippingString, rewardString, pledgeString
			shippingNum = float(shippingString)
			shippingTotal += shippingNum
			rewardNum = float(rewardString)
			rewardTotal += rewardNum
			pledgeNum = float(pledgeString)
			pledgeTotal += pledgeNum
			# print 'boards', (pledgeNum - shippingNum) / rewardNum
			boardsCount += (pledgeNum - shippingNum) / rewardNum
			backers += 1
#		print 'Total Rewards =', boardsCount
		outStr = 'Backers = '
		outStr += str(backers)
		outStr += '\nTotal Rewards = '
		outStr += str(boardsCount)
		outStr += '\n'
		outStr += 'Total Shipping = '
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
		First Name,MI,Last Name,Company,Address 1,Address 2,Address 3,City,State/Province,ZIP/Postal Code,Country,Urbanization,Phone Number,Fax Number,E Mail,Reference Number,Nickname
		"""
		outFilePtr.writerow(['First Name','MI','Last Name','Company','Address 1','Address 2','Address 3','City','State/Province','ZIP/Postal Code','Country','Urbanization','Phone Number','Fax Number','E Mail','Reference Number','Nickname'])
		outFilePtr.writerows(theList)

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
		if self.surveySent(theInList):
			processedList = self.processList(theInList)
			self.countBoards(theInList)
			self.writeOutUSPSAddressBook(outCSVFile, processedList)
		else:
			self.countBoards(theInList)

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
