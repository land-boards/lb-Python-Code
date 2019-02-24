"""
=================
pyCSVtoMWTable.py
=================

Convert a CSV into a MediaWiki table.

==========
Background
==========

MediaWiki is a very common Wiki page format. 
Wikipedia is the primary example that comes to mind for MediaWiki.
htt;://land-boards.com/blwiki is another popular page.

We wanted a way to easily load tables into Media Wiki.
The tables were in .csv (EXCEL) format.

=====
Usage
=====

This program prompts for a path and file to select for input.
The output file is created in the same path with a .MW output file name.

===
API
===

"""
from __future__ import print_function

from builtins import object
import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	 print("PyGtk 2.3.90 or later required")
	 raise SystemExit

import csv
import string
import os
import sys

#sys.path.append('C:\\Users\\doug_000\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')
#sys.path.append('C:\\Users\\Douglas\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')
#sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules')
sys.path.append('C:\\Users\\Doug\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')

from dgProgDefaults import *
from dgReadCSVtoList import *
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
	
class ControlClass(object):
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
		theInList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select CSV File')	# read in CSV into list
		if theInList == []:
			return False
		fileToWrite = myCSVFileReadClass.getLastPathFileName()[0:-4] + '.MW'
		#print 'fileToWrite',fileToWrite
		try:
			outFile = open(fileToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(fileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		self.writeOutMWTable(outFile, theInList)
		
	def writeOutMWTable(self, outFilePtr, theList):
		"""
		:param outFilePtr: Points to the output file.
		:param theList: The list to write out.

		"""
		outFilePtr.write('{| class="wikitable"\n')
		firstRow = True
		for row in theList:
			for cell in row:
				if firstRow:
					outFilePtr.write('! ' + cell + '\n')					
				else:
					outFilePtr.write('| ' + cell + '\n')
			firstRow = False
			outFilePtr.write('|-\n')
		outFilePtr.write('|}\n')

class UIManager(object):
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
		window.set_title('pyCSVtoMWTable - Kicad Parts List creation program')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("pyCSVtoMWTable")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyCSVtoMWTable", self.about_pyCSVtoMWTable),
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

	def about_pyCSVtoMWTable(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyCSVtoMWTable\n(c) 2014 - Doug Gilliland\nAAC - All rights reserved\npyCSVtoMWTable Create a mediawiki table frm a CV file")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
