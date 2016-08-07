"""
Reads in Mouser Order History file(s).

=====
Usage
=====

Program is run by either typing python pyMouserParts.py or double clicking pyMouserParts.py.

======
Output
======


====
Code
====

"""

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print "PyGtk 2.3.90 or later required for this example"
   raise SystemExit

import csv
import os
import sys
import string

# backAnnotate = True

def errorDialog(errorString):
	"""
	:param errorString: the string to print

	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class processMouserParts:
	"""Class to process the Mouser files.
	"""
	def selectMouserParts(self):
		"""
		:returns: path/name of the file that was selected. Empty string if none selected.
		
		This is the dialog which locates the Mouser files
		"""
		dialog = gtk.FileChooserDialog("Select csv file",
	                               None,
	                               gtk.FILE_CHOOSER_ACTION_OPEN,
	                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

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
			dialog.destroy()
			return ''
	
	def readInParts(self, partsFile):
		'''
		:param partsFile: location of the path/file name
		:returns: file contents as a list
		
		Read the parts file into a list for easier processing.
		'''
		partsFilePtr = open(partsFile,'rb')
		csvreader = csv.reader(partsFilePtr, delimiter=',', quotechar='|')
		partsList = []
		for row in csvreader:
			partsList.append(row)
		partsFilePtr.close()
		return partsList
		
	def goThroughTheParts(self,newPartsList,partsFileName):
		"""
		:param newPartsList: location of the path/file name
		:param partsFileName: location of the path/file name
		:returns: True when completed
		
		Process the parts list.
		"""
		outPartsList = partsFileName[0:-4]
		outPartsList += '_Parts.csv'
		procPL = []
		for row in newPartsList:
			if row[0] == 'Mouser #:':
				mouserPN = row[1]
				orderQty = row[3]
			elif row[0] == 'Mfr. #:':
				mfgPN = row[1]
			elif row[0] == 'Desc.:':
				descrPN = row[1]
				procPLLine = []
				procPLLine.append(mfgPN)
				procPLLine.append(mouserPN)
				procPLLine.append(descrPN)
				procPLLine.append(orderQty)
				procPL.append(procPLLine)
		procPL = sorted(procPL, key = lambda errs: errs[0])
		lastRow = []
		cumQty = 0
		newParts = []
		for row in procPL:
			if lastRow == []:
				lastRow = row
				cumQty = int(row[3])
			elif row[0] == lastRow[0]:
				cumQty += int(row[3])
			else:
				newPLRow = []
				newPLRow.append(lastRow[0])
				newPLRow.append(lastRow[1])
				newPLRow.append(lastRow[2])
				newPLRow.append(cumQty)
				lastRow = row
				cumQty = int(row[3])
				newParts.append(newPLRow)
		newPLRow = []
		newPLRow.append(lastRow[0])
		newPLRow.append(lastRow[1])
		newPLRow.append(lastRow[2])
		newPLRow.append(cumQty)
		newParts.append(newPLRow)
		outCSVFile = open(outPartsList, 'wb')
		outwriter = csv.writer(outCSVFile, delimiter=',')
		outwriter.writerows(newParts)
		return True		

	def doParts(self):
		'''
		:returns: True when completed
		
		The executive which calls all of the other functions.
		'''
		partsFileName = self.selectMouserParts()
		if partsFileName == '':
			errorDialog("Failed to open parts file")
			return False
		newPartsList = self.readInParts(partsFileName)
		self.goThroughTheParts(self,newPartsList,partsFileName)
		return True
	
class UIManager:
	""" The UI
	"""
	interface = """
	<ui>
		<menubar name="MenuBar">
			<menu action="File">
				<menuitem action="Open"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="Options">
				<menuitem action="BackAnn"/>
				<menuitem action="Analyze"/>
			</menu>
			<menu action="Help">
				<menuitem action="About"/>
			</menu>
		</menubar>
	</ui>
	"""

	def __init__(self):
		"""
		Create the top level window
		"""
		window = gtk.Window()
		window.connect('destroy', lambda w: gtk.main_quit())
		window.set_default_size(200, 200)
		
		vbox = gtk.VBox()
		
		# Create a UIManager instance
		uimanager = gtk.UIManager()

		# Add the accelerator group to the toplevel window
		accelgroup = uimanager.get_accel_group()
		window.add_accel_group(accelgroup)

		# Create an ActionGroup
		actiongroup =  gtk.ActionGroup("pyMouserParts")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
			("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
			("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
			("File", None, "_File"),
			("Options", None, "_Options"),
			("Help", None, "_Help"),
			("About", None, "_About", None, "About pyMouserParts", self.about_pymouserparts),
			])
		self.actiongroup.add_radio_actions([
			("BackAnn", gtk.STOCK_PREFERENCES, "_Back Annotate", '<Control>B', "Back annotate schematic from cmp file", 0),
			("Analyze", gtk.STOCK_PREFERENCES, "_Analyze", '<Control>A', "Analyze impact of backannotation", 1),
			], 2, self.setSelProcess)
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		""" Read the file and process it
		"""
		partsClass = processMouserParts()
		if partsClass.doParts() != False:
			message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
			message.set_markup("Function Completed")
			message.run()
			message.destroy()
		return

	def about_pymouserparts(self, b):
		"""The about message
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyMouserParts\nAuthor: Doug Gilliland\n(c) 2014 - All rights reserved\nProgram takes Mouser records and creates one big PL")
		message.run()
		message.destroy()
		
	# def setSelProcess(self, action, current):
		# global backAnnotate
		# text = current.get_name()
		# if (text == "BackAnn"):
			# backAnnotate = True
			# print 'Back annotate flag set'
		# elif (text == "Analyze"):
			# backAnnotate = False
			# print 'Analyze flag set'
		# return

	def quit_application(self, widget):
		"""
		quit
		"""
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
