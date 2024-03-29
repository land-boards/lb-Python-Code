#!/usr/bin/env python
"""
===================
dgWriteListtoCSV.py
===================

Functions to write a list to a CSV file.

Intended to be imported into another Python program.

Typical use

- outFileClass = WriteListtoCSV()
- outFileClass.appendOutFileName('_SIDES.csv')

==========
Background
==========

"""

import os
import datetime
import time
import pygtk
import sys
pygtk.require('2.0')

sys.path.append('C:\\Users\\DGilliland\\Documents\\Subversion\\python\\dgCommonModules')
sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules')
from dgProgDefaults import *

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	print "PyGtk 2.3.90 or later required for this example"
	raise SystemExit

verboseMode = False
outFileNameAppendage = ''

def errorDialog(errorString):
	"""
	Prints an error message as a gtk style dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class WriteListtoCSV():
	"""This is the class that has the methods which are used to write out a CSV list.
	The typical method that is called is writeOutList(outPathFilename, header, csvListToWrite)
	Alternately the file can be selected
	"""
	def selectOutputFileName(self,defaultPath):
		"""
		
		:return: the name of the output csv file
		
		"""
		dialog = gtk.FileChooserDialog(title="Save as", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		if defaultPath != '':
			dialog.set_current_folder(defaultPath)
		filter.set_name("*.csv")
		filter.add_pattern("*.csv") # whats the pattern for a folder 
		dialog.add_filter(filter)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFileName = dialog.get_filename()
			dialog.destroy()
			return(retFileName)
		elif response == gtk.RESPONSE_CANCEL: 
			print 'Closed, no files selected'
		dialog.destroy()
		exit()
	
	def writeOutList(self, outPathFilename, header, csvListToWrite):
		"""Write out the csvListToWrite
		"""
		global verboseMode
		outFileNm = self.createOutputFilename(outPathFilename)
		if verboseMode:
			print 'Output file name :',
			print (self.extractFilenameFromPathfilename(outFileNm))
		if csvListToWrite == []:
			errorDialog('Write list is empty for some reason')
			return
		outFilePtr = self.openCSVFile(outFileNm)	# start at the same folder as the input file was located
		self.writeOutputHeader(outFilePtr,header)			# write out the header
		if self.test_dim(csvListToWrite) == 1:
			outFilePtr.writerow(csvListToWrite)
		else:
			#print csvListToWrite
			outFilePtr.writerows(csvListToWrite)
		
	def openCSVFile(self, csvName):
		"""Creates an output CSV file and has the functions to write to the CSV file
		
		:param csvName: String which has the Pathfilename of the csv file
		"""
		try:
			myCSVFile = open(csvName, 'wb')
		except:
			errorDialog("Couldn't open the output file\nIs the file open in Excel?")
			try:
				myCSVFile = open(csvName, 'wb')
			except:
				errorDialog("Couldn't open the output file, Exiting...")
				exit()
		outFil = csv.writer(myCSVFile)
		return(outFil)
		
	def extractFilenameFromPathfilename(self, fullPathFilename):
		"""Extract fileName from pathfullPathName
		
		:param fullPathFilename: The path/filename of the input file
		:returns: the file name extracted out from the path
		"""
		return(fullPathFilename[fullPathFilename.rfind('\\')+1:])
		
	def extractPathFromPathfilename(self, fullPathFilename):
		"""Extract path from pathfullPathName
		
		:param fullPathFilename: The path/filename of the input file
		:returns: the file name extracted out from the path
		"""
		return(fullPathFilename[0:fullPathFilename.rfind('\\')+1:])
		
	def createOutputFilename(self, inFileName):
		"""Creates the output file name based on the input file name
		
		:param inFileName: The pathfilename of the input file.
		"""
		global outFileNameAppendage
		if outFileNameAppendage == '':
			return inFileName
		if inFileName[-4:0] != '.csv' and inFileName[-4:0] != '.CSV':
			return(inFileName[0:-4] + outFileNameAppendage)
		else:
			errorDialog('input Filename needs to have csv as the extension')
			return(inFileName[0:-4] + outFileNameAppendage)
	
	def test_dim(self,testlist, dim=0):
		"""tests if testlist is a list and how many dimensions it has
		returns -1 if it is no list at all, 0 if list is empty 
		and otherwise the dimensions of it"""
		if isinstance(testlist, list):
			if testlist == []:
				return dim
			dim = dim + 1
			dim = self.test_dim(testlist[0], dim)
			return dim
		else:
			if dim == 0:
				return -1
			else:
				return dim

	def writeOutputHeader(self, outPtr, header):
		"""Write out the Output header.
		The header can be a list which would be a single line header or a list of lists which would be a multiline header.
		
		:param outPtr: The pointer to the output file.
		:param header: The output file header
		
		"""
		if header == [] or header == '' or header == None:
			errorDialog('header was empty')
			return
		elif self.test_dim(header) == 1:
			outPtr.writerow(header)
		else:
			outPtr.writerows(header)
		
	def setVerboseMode(self,verboseFlag):
		global verboseMode
		verboseMode = verboseFlag
		
	def appendOutFileName(self,outFileNameAppendString):
		global outFileNameAppendage
		outFileNameAppendage = outFileNameAppendString
		
	def setOutFileName(self,outFileName):
		global inFileName
		inFileName = outFileName
	