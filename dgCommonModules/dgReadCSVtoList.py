#!/usr/bin/env python
"""
==================
dgReadCSVtoList.py
==================

Functions to read a CSV file into a list and return the list.

Intended to be imported into another Python program.

==========
Background
==========

==================
Installation/Usage
==================

- Put this file into the folder C:/Python27/Lib/site-packages/dgCommonModules

Typical use

- myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
- myCSVFileReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
- csvAsReadIn = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select CSV File')	# read in CSV into list
- if csvAsReadIn == []:
-  return False

===
API
===

"""

import os
import datetime
import time
import pygtk
import sys
pygtk.require('2.0')

sys.path.append('C:\\Users\\DGilliland\\Documents\\Subversion\\python\\dgCommonModules')
sys.path.append('C:\\Python27\\Lib\\site-packages\\dgCommonModules')

try:
	from dgProgDefaults import *
except:
	print('Need to load dgProgDefaults into site-packages')
try:
	from dgCheckFileFresh import *
except:
	print('Need to load dgCheckFileFresh into site-packages')

lastPathFileName = ''

verboseMode = False
freshFlag = False
useSniffer = False

import gtk
# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	print "PyGtk 2.3.90 or later required for this example"
	raise SystemExit

def errorDialog(errorString):
	"""
	Prints an error message as a gtk style dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class ReadCSVtoList():
	def findOpenReadCSV(self, defaultPath='', dialogHeader='Open File'):
		"""findOpenReadCSV(self, defaultPath, dialogHeader)
		This is the main method which calls the other methods in this class.
		
		:global lastPathFileName: The path asset by this function based on the path found by the browser.
		:global verboseMode: Set to true if you want diagnostic messages printed along the way. Verbose Mode can also be changed by calling setVerboseMode().

		:param defaultPath: Optional default path. If none is entered defaults to empty.
		:param dialogHeader: Optional headers that is printed on the top of the screen.

		:return: The contents of the file as a list. If cancel was pressed on the file selector or the file is empty, returns an empty list.
		
		"""
		global lastPathFileName
		global verboseMode
		#print 'findOpenReadCSV: got here'
		inPathFilename = self.findInputCSVFile(defaultPath, dialogHeader)
		if inPathFilename == '':
			errorDialog('Input file was not selected')
			return []
		lastPathFileName = inPathFilename
		defaultPath = inPathFilename[0:inPathFilename.rfind('\\')+1]
		myDefaultHandler = HandleDefault()
		myDefaultHandler.storeKeyValuePair('DEFAULT_PATH',defaultPath)
		if verboseMode:
			print 'Input file name :',
			print self.extractFilenameFromPathfilename(inPathFilename)
		if freshFlag:
			myFreshCheck = CheckFreshness()
			if not myFreshCheck.isFresh(xmlFileName):
				if verboseMode:
					print 'fresh flag was set to check freshness for CSV files'
				errorDialog("The CSV File is not fresh\nEither change the Options to ignore the freshness check\nor create/choose a fresh file")
				return []
		csvFileAsReadIn = self.readInCSV(inPathFilename)
		if csvFileAsReadIn == []:
			errorDialog("Didn't read in any BOM contents")
		return csvFileAsReadIn

	def findInputCSVFile(self,defaultPath,bomFileString='Select File to Open'):
		"""Uses filechooser to browse for a CSV file.
		
		:param defaultPath: The path that was selected. The calling function is responsible for remembering the name.

		:returns: pathfilename of the file that was selected or empty string if no file was selected.
		
		"""
		dialog = gtk.FileChooserDialog(bomFileString,
													None,
													gtk.FILE_CHOOSER_ACTION_OPEN,
													(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
													gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		dialog.set_current_folder(defaultPath)
		
		filter = gtk.FileFilter()
		filter.set_name("CSV Files")
		filter.add_pattern("*.csv")
		dialog.add_filter(filter)
		
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			inFileNameString = dialog.get_filename()
			dialog.destroy()
			return inFileNameString
		elif response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
			dialog.destroy()
			return ''
			
	def extractFilenameFromPathfilename(self, fullPathFilename):
		"""Extract fileName without extension from pathfullPathName

		:param fullPathFilename: The path and file name
		
		:returns: Path without the filename at the end

		"""
		return(fullPathFilename[fullPathFilename.rfind('\\')+1:])

	def readInCSV(self, inFileN):
		"""Reads a CSV file into a list. This method 
		
		:global useSniffer: Flag which indicates whether or not to use the file sniffer. Set the sniffer flag by setUseSnifferFlag().
		
		:param inFileN: Input pathfilename

		:returns: List which contains the contents of the CSV file
		
		"""
		global useSniffer
		# select the input file names and open the files
		intFileHdl = open(inFileN, 'rb')
		if useSniffer:
			dialect = csv.Sniffer().sniff(intFileHdl.read(1024))
			intFileHdl.seek(0)
			reader = csv.reader(intFileHdl, dialect)
		else:
			reader = csv.reader(intFileHdl)
		
		# read in the CSV file into csvListIn
		csvListIn = []
		for row in reader:
			csvListIn.append(row)
		return csvListIn

	def getLastPathFileName(self):
		"""getLastPathFileName - Used by external calling methods to determine what the path/filename 
		of the last file that was read in was.
		
		:global lastPathFileName: the last path file name that was used
		
		:returns: the last path file name
		
		"""
		global lastPathFileName
		return lastPathFileName

	def getLastPath(self):
		"""getLastPathFileName - Used by external calling methods to determine what the path/filename 
		of the last file that was read in was.
		
		:global lastPathFileName: the last path file name that was used
		
		:returns: the last path file name
		
		"""
		global lastPathFileName
		return(lastPathFileName[0:lastPathFileName.rfind('\\')+1])

	def setVerboseMode(self,verboseFlag):
		"""Set the verbose mode flag. 
		This flag is used by other functions to determine whether messages should be output to the console or not.
		
		:global verboseMode: Flag value.
		
		:returns: Always True
		
		"""
		global verboseMode
		verboseMode = verboseFlag
		return True
	
	def setFreshCheckFlag(self,freshnessFlag):
		"""Set the freshness check flag.
		This flag is used to determine whether or not to check the file freshness before opening it.
		If this flag is set the file has to be created on the same day that this method is invoked.
		This is intended to be set from other modules which use this class.
		
		:global freshFlag: Flag value stored as a global for use directly by other functions
		:global verboseMode: Verbose flag.
		
		:returns: True always
		"""
		global freshFlag
		global verboseMode
		if verboseMode:
			print 'CheckFreshness:setFreshCheckFlag: setting freshness flag', freshnessFlag
		freshFlag = freshnessFlag
		return True
		
	def getFreshFlag(self):
		"""Return the value of the freshness check flag
		
		:global freshFlag: Flag value stored as a global for use directly by other functions
		:global verboseMode: Verbose flag.
		
		:returns: the value of the fresh check flag.

		"""
		global freshFlag
		global verboseMode
		if verboseMode:
			print 'CheckFreshness:getFreshFlag: getting freshness flag',freshFlag
		return freshFlag

	def setUseSnifferFlag(self,snifferFlag):
		"""Set the flag for whether or not the CSV sniffer should be used when reading the CSV file.
		 The sniffer can determine the input file style of the delimiter (comma separated, tab separated, etc.)
		
		:global useSniffer: Flag that determines whether or not to use the CSV sniffer.

		:returns: True always
		
		"""
		global useSniffer
		useSniffer = snifferFlag
		return True
		