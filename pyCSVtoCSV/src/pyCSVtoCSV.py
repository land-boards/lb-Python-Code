"""
pyCSVtoCSV.py
Convert a CSV into a different formatted CSV.
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

class ControlClass:
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

	def readInCSV(self, inFile):
		csvReader = csv.reader(inFile)
		list2Read = []
		for row in csvReader:
			list2Read.append(row)
		return list2Read
		
	def createOutputFileName(self, inFileName):
		"""Creates the output file name based on the input file name
		
		:param inFIleName: The pathfilename of the input file.
		"""
		return(inFileName[0:-4] + '_CAN.csv')
		
	def writeOutputHeader(self, outPtr):
		"""Write out the Output header.
		
		:param outPtr: The pointer to the output CSV file.
		"""
		outPtr.writerow(['column1','column2'])
		return

	""" the stuff to open output file
	"""

	def writeOutputFile(self, outFile, outFilePtr):
		"""Write out header and body
		"""
		self.writeOutputHeader(outFilePtr)					# write out the header
		outFilePtr.writerows(outFile)						# write out the BOM list to the output CSV file
		
	def processCSV(self, theInList):
		''' This function is where the conversion from one CSV format to another happens
		List the input fields here
		...
		List the output fields here
		...
		'''
		myOutList = []
		for row in theInList:	# Go through the input list one line at a time
			myOutList.append(row)
		return myOutList
		
	def theExecutive(self):
		'''This is the main executive which gets called when someone selects file open.
		'''
		fileToRead = self.findCSVFileBrowse('.')

		try:
			inFile = open(fileToRead, 'rb')
		except IOError:
			errorDialog('ERROR - Cannot open input file')
			exit()
		
		fileToWrite = fileToRead[:-4] + "_out.csv"
		print 'out file name', fileToWrite

		try:
			outFile = open(fileToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(fileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		# Pointer to the CSV writer
		outFil = csv.writer(outFile)
		
		# Read in the CSV file
		theInList = self.readInCSV(inFile)
		
		# Process the CSV file
		theOutList = self.processCSV(theInList)
		
		# Write out the CSV file
		self.writeOutputFile(theOutList, outFil)

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
		window.set_title('pyCSVtoCSV - Convert CSV file from one format to another')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("pyCSVtoCSV")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyCSVtoCSV", self.about_pyCSVtoCSV),
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

	def about_pyCSVtoCSV(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyCSVtoCSV\nAuthor: Doug Gilliland\n(c) 2014 - AAC - All rights reserved\npyCSVtoCSV - Convert input CSV file to a different CSV")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
