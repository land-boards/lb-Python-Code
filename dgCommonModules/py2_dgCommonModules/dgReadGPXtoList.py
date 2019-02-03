#!/usr/bin/env python
"""
==================
dgReadGPXtoList.py
==================

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

gpxFilePath = ''
gpxFileName = ''
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
	def findReadGPXSpreadsheet(self,startingPath):
		"""Find the XMP Spreadseet and read it into a list
		   <trkpt lat="40.0070560" lon="-79.5889880">
			<ele>290.5</ele>
			<time>2018-07-27T10:40:00Z</time>
			<extensions>
			 <gpxtpx:TrackPointExtension>
			  <gpxtpx:hr>67</gpxtpx:hr>

		"""
		global gpxFilePath
		global gpxFileName
		gpxFilePath = startingPath
		gpxFileName = self.findGPXFile()
		gpxFilePath = self.extractPathFromPathfilename(gpxFileName)
		startingPathName = self.extractPathFromPathfilename(gpxFileName)
		if gpxFileName == '':
			return False
		gpx_file = open(gpxFileName, 'r')
		gpxList = []
		gpxLine = []
		dateTime = ''
		lat = ''
		lon = ''
		hr = ''
		ele = ''
		for line in gpx_file:
			if '<trkpt' in line:	# <trkpt lat="40.0070560" lon="-79.5889880">
				latStartOffset = line.find('lat=\"') + 5
				latEndOffset = line.find('\" lon')
				lonStartOffset = line.find('lon=') + 5
				lonEndOffset = line.find('\">')
				gpxLine = []
#				print 'Lat:', line[latStartOffset:latEndOffset],
#				print 'Lon:', line[lonStartOffset:lonEndOffset]
				lat = line[latStartOffset:latEndOffset]
				lon = line[lonStartOffset:lonEndOffset]
			elif 'ele' in line:			# <ele>290.5</ele>
#				print 'ele found'
				ele = line[line.find('<ele>')+5:line.find('</ele>')]
			elif 'time' in line:		# <time>2018-07-27T10:40:00Z</time>
#				print 'time found'
				dateTime = line[line.find('<time>')+6:line.find('</time>')]
			elif 'gpxtpx:hr' in line:	# <gpxtpx:hr>67</gpxtpx:hr>
#				print 'hr found'
				hr = line[line.find('<gpxtpx:hr>')+11:line.find('</gpxtpx:hr>')]
			elif '</trkpt>' in line:
				gpxLine.append(dateTime)
				gpxLine.append(lat)
				gpxLine.append(lon)
				gpxLine.append(ele)
				gpxLine.append(hr)
				#print 'gpxLine',gpxLine
				gpxList.append(gpxLine)
		return gpxList
		
	def setFreshCheckFlag(self,freshCheckValue):
		global freshnessCheck
		if verboseMode:
			print 'XMLtoList:setFreshCheckFlag: set the check fresh flag to :',freshCheckValue
		freshnessCheck = freshCheckValue
	
	def getFilePath(self):
		global gpxFilePath
		return gpxFilePath
	
	def getLastPath(self):
		return (self.extractPathFromPathfilename(self.getFilePath()))
		
	def getFullPathAndFileName(self):
		global gpxFileName
		return gpxFileName
	
	def	extractPathFromPathfilename(self,fullPathFilename):
		""" Extracts the Path out of the PathFilename
		
		:param fullPathFilename: The file pathfilename
		:returns: only the path portion of the pathfilename
		"""
		return(fullPathFilename[0:fullPathFilename.rfind('\\')+1])
	
	def findGPXFile(self):
		"""This is the dialog which locates the xml files
		Function returns the path/name of the file that was selected
		
		:param startingPath: The Path to start searching at
		
		:returns: String which has the Path/filename
		"""
		global gpxFilePath
		csvFileString = "Select GPX file"
		dialog = gtk.FileChooserDialog(csvFileString,
	                               None,
	                               gtk.FILE_CHOOSER_ACTION_OPEN,
	                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		dialog.set_current_folder(gpxFilePath)
		filter = gtk.FileFilter()
		filter.set_name("GPX files")
		filter.add_pattern("*.gpx")
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
