#!/usr/bin/env python
"""
=================
dgProgDefaults.py
=================

This program handles program defaults.

==========
Background
==========

Programs need to have certain defaults from one run to another.
This file has those functions.

================
Input File Types
================

This program supports the following types of BOMs as inputs:

- DEFAULTS.csv -The defaults file

The defaults file has KEY,Value pairs in clear text

Typical use

- defaultParmsClass = HandleDefault()
- defaultParmsClass.initDefaults()
- defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')

====
Code
====

"""

import string
import csv
import os

import pygtk
pygtk.require('2.0')

# global program options

dgProgDefaultsModuleName = 'dgProgDefaults.py'
progVer = '0.0.1'

defaultsFileNamePath = '.\\Defaults.csv'

verboseMode = False

class HandleDefault:
	""""Load and save defaults file
	This can be used to save stuff like the default path
	The file is a simple list with KEY, value pairs on individual lines
	"""
	def initDefaults(self):
		global defaultPath
		global defaultsFileNamePath
		global verboseMode
		defaultFilePath = os.getcwd()
		defaultsFileNamePath = defaultFilePath + '\\Defaults.csv'
		if verboseMode:
			print 'set defaultsFileNamePath to', defaultsFileNamePath
		if self.ifExistsDefaults() == True:
			detailParmList = self.loadDefaults()
			if verboseMode:
				print 'loaded defaults file'
		else:
			if verboseMode:
				print 'defaults file did not exist',
			self.createDefaults()
			if verboseMode:
				print 'created defaults file',
			detailParmList = self.loadDefaults()
			if verboseMode:
				print 'loaded defaults file'
		if self.getKeyVal('DEFAULT_PATH') == False:
			if verboseMode:
				print 'There was no default path set'
			self.storeKeyValuePair('DEFAULT_PATH',defaultPath)
		return True
		
	def loadDefaults(self):
		"""
		:return: the default list of key names and key values

		Load the defaults file
		"""
		defaultFileHdl = open(defaultsFileNamePath, 'rb')
		defaultListItem = csv.reader(defaultFileHdl)
		defaultList = []
		for row in defaultListItem:
			defaultList+=row
		return defaultList

	def getKeyVal(self, keyName):
		"""
		:param: keyName - the name of the key to look up
		:return: the value of that key, blank if there is no corresponding key
		
		Feed it a key name and it returns the corresponding key value
		"""
		#print 'getKeyVal: got here'
		if self.ifExistsDefaults() == False:
			if verboseMode:
				print 'getKeyVal: had to creat defaults'
			self.createDefaults()
		defaultFileHdl = open(defaultsFileNamePath, 'rb')
		defaultListItem = csv.reader(defaultFileHdl)
		defaultList = []
		for row in defaultListItem:
			if row[0] == keyName:
				if verboseMode:
					print 'getKeyVal: found a match for key, match was', row[1]
				return row[1]
		if verboseMode:
			print 'getKeyVal: did not find a match for the key'
		return ''
	
	def storeKeyValuePair(self,keyName,valueToWrite):
		if verboseMode:
			print 'storeKeyValuePair: storing value =',valueToWrite,
			print 'to key =',keyName,
		if self.ifExistsDefaults() == False:
			self.createDefaults()
		defaultFileHdl = open(defaultsFileNamePath, 'rb')
		defaultListItem = csv.reader(defaultFileHdl)
		newList = []
		foundKey = False
		for item in defaultListItem:
			newLine = []
			if item[0] == keyName:
				newLine.append(item[0])
				newLine.append(valueToWrite)
				foundKey = True
			else:
				newLine = item
			newList.append(newLine)
		if foundKey == False:
			newLine.append(keyName)
			newLine.append(valueToWrite)
			newList.append(newLine)
		self.storeDefaults(newList)
		return True
		
	def storeDefaults(self,defaultList):
		""" 
		:param: feed it the default key name and key value pairs
		:return: True if successful
		
		Store the key name and key value pair list to the defaults file
		"""
		if verboseMode:
			print 'storing list', defaultList
		defaultFileHdl = open(defaultsFileNamePath, 'wb')
		defaultFile = csv.writer(defaultFileHdl)
		defaultFile.writerows(defaultList)
		return True

	def createDefaults(self):
		""" 
		:return: True if successful
		
		Create the defaults file with a single pair
		"""
		defaultFileHdl = open(defaultsFileNamePath, 'wb')
		defaultFile = csv.writer(defaultFileHdl)
		defaultArray = ['DEFAULT_PATH','.']
		defaultFile.writerow(defaultArray)
		return True
		
	def ifExistsDefaults(self):
		"""
		:return: True if the default file exists, false if the default file does not exist
		
		Check if the defaults file exists
		"""
		try:
			open(defaultsFileNamePath)
		except:
			return False
		return True
		
	def setVerboseMode(self,verboseFlag):
		global verboseMode
		verboseMode = verboseFlag
