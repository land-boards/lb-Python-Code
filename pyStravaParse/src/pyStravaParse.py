"""
================
pyStravaParse.py
================

Crunch Strava XML file.

==========
Background
==========

Strava is a running tracker.
Strava exports data as XML.
This program takes the XML output file from Strava and creates a reduced data set.

=====
Usage
=====

This program prompts for Strava file.
The output file is created in the same path with as StravaCrunch-YY-MM-DD.csv

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
from dgReadGPXtoList import *
from dgWriteListtoCSV import *
from dgHeaderDict import *
defaultPath = '.'

from sys import argv

HRMax = '122'
HRMin = '112'

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

		myXMLFileReadClass = XMLtoList()	# instantiate the class
		myXMLFileReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		stravaList = myXMLFileReadClass.findReadGPXSpreadsheet(defaultPath)	# read in CSV into list

		stravFileOutToWrite = myXMLFileReadClass.getFullPathAndFileName()[:-4] + '_CR.CSV'
		#print 'stravFileOutToWrite',stravFileOutToWrite
		try:
			outFile = open(stravFileOutToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(stravFileOutToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		myCSVFileWriteClass = WriteListtoCSV()
		myCSVFileWriteClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		newStravaList = self.convertDate(stravaList)

		header = ['Date_Time','Lat','Lon','Elev','Heart_Rate','HRmax','HRmin']
		myCSVFileWriteClass.writeOutList(stravFileOutToWrite, header, newStravaList)
		
		defaultPath = myXMLFileReadClass.getLastPath()
		defaultParmsClass.storeKeyValuePair('DEFAULT_PATH',defaultPath)
		
	def convertDate(self, stravaList):
		"""
		:param stravaList: The servings list.
		
		:returns: list of ['Date','Protein','Fat','Carbs','Calories']
		
		Take the foods and sum up the Protein, Fat and Carbs for each food item.
		"""
		outList = []
		firstTime = self.pullTime(stravaList[0][0])
		outRow = []
		outRow.append('0')
		outRow += stravaList[0][1:]
		outRow.append(HRMax)
		outRow.append(HRMin)
		outList.append(outRow)
		for row in stravaList[1:]:
			outRow = []
			theTime = self.pullTime(row[0])
			outRow.append(theTime - firstTime)
			outRow += row[1:]
			outRow.append(HRMax)
			outRow.append(HRMin)
			outList.append(outRow)
		return outList
		
	def pullTime(self, timeString):
		"""2018-06-24T22:43:00Z
		   00000000011111111112
		   12345678901234567890
		"""
		timeString = timeString.replace('T',':')
		timeString = timeString.replace('Z',':')
		timeString = timeString.replace('-',':')
		#print 'timeString',timeString
		timeDate = []
		timeDate = timeString.split(':')
		#print 'timeDate',timeDate
		year = int(timeDate[0])
		month = int(timeDate[1])
		day = int(timeDate[2])
		hour = int(timeDate[3])
		min = int(timeDate[4])
		ticks = int(timeDate[5])
		ticks += min*60
		ticks += hour*60*60
		ticks += day*24*60*60
		return ticks

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
		window.set_title('pyStravaParse - Kicad Parts List creation program')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("pyStravaParse")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyStravaParse", self.about_pyStravaParse),
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

	def about_pyStravaParse(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyStravaParse\n(c) 2014 - Doug Gilliland\nAAC - All rights reserved\npyStravaParse Create a mediawiki table frm a CV file")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
