#!/usr/bin/env python
"""
===============
dgHeaderDict.py
===============

This library creates a dictionary from a file header.
This library has routines to deal with the header dictionary.

==========
Background
==========

===
API
===

"""

from builtins import object
headerDictionary = {}

import os

class headerDict(object):
	"""Make dictionary from a header of a CSV spreadsheet
	"""
	def makeHeaderDict(self, headerLine):
		"""
		:param headerLine: The header as a list
		:returns: header as a dictionary
		
		"""
		global headerDictionary
		headerDictionary = {}
		i = 0
		for element in headerLine:
			headerDictionary[element] = i
			i = i + 1
		return headerDictionary

	def printHeaderOffsets(self, headerLine):
		"""
		:param headerLine: The header as a list
		:returns: header as a dictionary
		
		"""
		myHeaderAsDictionary = self.makeHeaderDict(headerLine)

	def getHeaderOffset(self, headerKey):
		"""
		:param headerString: The key to look up the column offset
		:returns: header as a dictionary
		
		"""
		global headerDictionary
		return headerDictionary[headerKey]
		
	def extractDataFromLine(self, dataLine, key):
		"""
		:param dataLine: The spreadsheet line as a list
		:param key: The key to look up
		:returns: data element corresponding to the key
		
		Assumes that makeHeaderDict was already populated
		
		"""
		global headerDictionary
		if headerDictionary == {}:
			return -1
		else:
			return headerDictionary[getHeaderOffset(key)]
