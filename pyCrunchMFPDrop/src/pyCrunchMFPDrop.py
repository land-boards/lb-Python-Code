"""
==================
pyCrunchMFPDrop.py
==================

Crunch a set of MFP files.

==========
Background
==========

MFP did a big data drop.

=====
Usage
=====

This program prompts for the MFP file.
The output file is created in the same path with as MFP_Crunch.csv

===
API
===

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

sys.path.append('C:\\Users\\Doug\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')
sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules')

from dgProgDefaults import *
from dgReadCSVtoList import *
from dgWriteListtoCSV import *
from dgHeaderDict import *
defaultPath = '.'

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
	
class ControlClass:
	def theExecutive(self):
		"""
		:global lastPathFileName: The path and file name that was found by the browser.

		The code that calls the other code.
		This code uses the defaults library to handle the default path.
		This code uses the read CSV library to read in the CSV file.
		"""
		global defaultPath
		
		defaultParmsClass = HandleDefault()
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		#print 'defaultPath',defaultPath

		myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
		myCSVFileReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		myCSVFileReadClass.setUseSnifferFlag(True)
		mfpDataList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select MFP TSV File')	# read in TSV into list
		if mfpDataList == []:
			return False
		crunchedMFPList = self.crunchMFPList(mfpDataList)

		weightFileToWrite = myCSVFileReadClass.getLastPath() + 'pyCronCrunch_Weight.CSV'
		#print 'weightFileToWrite',weightFileToWrite
		try:
			outFile = open(weightFileToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(weightFileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		myCSVFileWriteClass = WriteListtoCSV()
		myCSVFileWriteClass.setVerboseMode(True)	# turn on verbose mode until all is working 

		header = ['User','Count_of_Meals']
		myCSVFileWriteClass.writeOutList(weightFileToWrite, header, crunchedMFPList)
		
	def crunchMFPList(self, mfpDataList):
		"""
		:param mfpDataList: The servings list.
		
		:returns: list of ['Date','Protein','Fat','Carbs','Calories']
		
		Take the foods and sum up the Protein, Fat and Carbs for each food item.
		"""
		servingsHeader = ['meal_id','user_id','date','meal_sequence','food_ids']
		myHeaderDictionary = headerDict()
		servingsDictionary = myHeaderDictionary.makeHeaderDict(servingsHeader)
		mealIDColumnOffset = int(myHeaderDictionary.getHeaderOffset('meal_id'))
		userIDColumn = int(myHeaderDictionary.getHeaderOffset('user_id'))
		dateColumn = int(myHeaderDictionary.getHeaderOffset('date'))
		mealSequenceColumn = int(myHeaderDictionary.getHeaderOffset('meal_sequence'))
		foodIDsColumn = int(myHeaderDictionary.getHeaderOffset('food_ids'))
		mealCount = 0
		shortcrunchedMFPList = []
		lastUserID = '1'
		for row in mfpDataList[1:]:
			if len(row) > 4 and row[userIDColumn] == lastUserID:
				mealCount += 1
			else:
				shortRow = []
				shortRow.append(lastUserID)
				lastUserID = row[userIDColumn]
				shortRow.append(str(mealCount))
				shortcrunchedMFPList.append(shortRow)
				mealCount = 1
		return shortcrunchedMFPList
		
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
		window.set_title('pyCrunchMFPDrop - Kicad Parts List creation program')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("pyCrunchMFPDrop")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyCrunchMFPDrop", self.about_pyCrunchMFPDrop),
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
		message.set_markup("Conversion Complete")
		message.run()		# Display the dialog box and hang around waiting for the "OK" button
		message.destroy()	# Takes down the dialog box
		return

	def about_pyCrunchMFPDrop(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyCrunchMFPDrop\n(c) 2014 - Doug Gilliland\nAAC - All rights reserved\npyCrunchMFPDrop Create a mediawiki table frm a CV file")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
