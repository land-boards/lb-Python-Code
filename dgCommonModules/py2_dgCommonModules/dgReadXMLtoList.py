#!/usr/bin/env python
"""
===================
dgReadXMLtoList.py
===================

This program 

==========
Background
==========

"""

import os
import datetime
import time
import sys

sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules')
sys.path.append('C:\\Users\\Doug\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')

from dgCheckFileFresh import *

import pygtk
pygtk.require('2.0')

import gtk
# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	print "PyGtk 2.3.90 or later required for this example"
	raise SystemExit

# Use the ElementTree module but alias it as "Xml"
import xml.etree.ElementTree as Xml

xmlFilePath = ''
freshnessCheck = True
verboseMode = False

def errorDialog(errorString):
	"""Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class XMLtoList:
	"""Reads the XML file into a list and returns the list
	"""
	def findReadXMLSpreadsheet(self,startingPath):
		"""Find the XMP Spreadseet and read it into a list
		"""
		global xmlFilePath
		xmlFilePath = startingPath
		xmlFileName = self.findXmlFile()
		xmlFilePath = self.extractPathFromPathfilename(xmlFileName)
		startingPathName = self.extractPathFromPathfilename(xmlFileName)
		if xmlFileName == '':
			return False
		if freshnessCheck:
			myFreshCheck = CheckFreshness()
			if not myFreshCheck.isFresh(xmlFileName):
				print 'xml file is not fresh... Exiting'
				errorDialog("The XML File is not fresh\nEither change the Options to ignore the freshness check\nor create/choose a fresh file")
				return []
		xmlList = self.readSpreadsheetXML2List(xmlFileName)
		return xmlList
		
	def readSpreadsheetXML2List(self, inFileN):
		global xmlFilePath
		"""Returns a list which contains the XML spreadsheet data
		
		:param inFileN: The input Pathfilename (path and file name)
		:returns: A list which contains the XML spreadsheet data
		"""
	
		#Get the root by parsing the XML file and then using the "getroot" method 
		root = Xml.parse(inFileN).getroot()

		# Get the worksheet section by findall all of the worksheet tags (should only be one) then selecting the first 
		worksheet = root.findall("{urn:schemas-microsoft-com:office:spreadsheet}Worksheet")[0]

		# Get the table section
		table = worksheet.findall('{urn:schemas-microsoft-com:office:spreadsheet}Table')[0]

		# Make a new list to store the data read from the cells 
		xmlData = []

		# Loop through all the elements directly under the table 
		for row in table.findall("{urn:schemas-microsoft-com:office:spreadsheet}Row"):
			new_list = []			# Append a new list onto the results to store that row's data
			xmlData.append(new_list)
			for cell in row:		# Loop through all the cells in the row
				if len(cell) > 0:
					new_list.append(cell[0].text or "")	# Append the cell data to the new list
		return xmlData

	def setFreshCheckFlag(self,freshCheckValue):
		global freshnessCheck
		if verboseMode:
			print 'XMLtoList:setFreshCheckFlag: set the check fresh flag to :',freshCheckValue
		freshnessCheck = freshCheckValue
	
	def getFilePath(self):
		global xmlFilePath
		return xmlFilePath
		
	def	extractPathFromPathfilename(self,fullPathFilename):
		""" Extracts the Path out of the PathFilename
		
		:param fullPathFilename: The file pathfilename
		:returns: only the path portion of the pathfilename
		"""
		return(fullPathFilename[0:fullPathFilename.rfind('\\')+1])
	
	def findXmlFile(self):
		"""This is the dialog which locates the xml files
		Function returns the path/name of the file that was selected
		
		:param startingPath: The Path to start searching at
		
		:returns: String which has the Path/filename
		"""
		global xmlFilePath
		csvFileString = "Select XML file"
		dialog = gtk.FileChooserDialog(csvFileString,
	                               None,
	                               gtk.FILE_CHOOSER_ACTION_OPEN,
	                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		dialog.set_current_folder(xmlFilePath)
		filter = gtk.FileFilter()
		filter.set_name("XML files")
		filter.add_pattern("*.xml")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retPathFileName = dialog.get_filename()
			dialog.destroy()
			return retPathFileName
		elif response == gtk.RESPONSE_CANCEL or response == gtk.RESPONSE_DELETE_EVENT:
			dialog.destroy()
			errorDialog("No file was selected")
			return ''
		else:
			print 'unexpected response was', response
		dialog.destroy()

	def setVerboseMode(self,verboseFlag):
		global verboseMode
		verboseMode = verboseFlag
