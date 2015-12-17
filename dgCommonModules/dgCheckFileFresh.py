#!/usr/bin/env python
"""
===================
pyCheckFileFresh.py
===================

This program allows a file to be checked for freshness.
If the file was edited on the same date as this function is run then the file is considered to be fresh.

==========
Background
==========

"""

import os
import datetime
import time

verboseMode = False
freshFlag = True

class CheckFreshness():
	"""Class which checks a file to see if it is fresh
	"""
	## Returns True if the file was saved today, False otherwise
	def isFresh(self, pathToFile):
		"""isFresh checks to see if the file was created today
		
		:param pathToFile: The path/filename to check
		:returns: True if the file is fresh (saved today), False otherwise
		"""
		t = os.path.getmtime(pathToFile)
		fileTimeDateStamp = datetime.datetime.fromtimestamp(t)
		fileDateStamp = str(fileTimeDateStamp)
		fileDateStamp = fileDateStamp[0:fileDateStamp.find(' ')]
		currentDate = time.strftime("%Y-%m-%d")
		if fileDateStamp == currentDate:
			return True
		else:
			return False
		
	def setVerboseMode(self,verboseFlag):
		global verboseMode
		verboseMode = verboseFlag
		
	def setFreshCheckFlag(self,freshnessFlag):
		global freshFlag
		global verboseMode
		if verboseMode:
			print 'CheckFreshness:setFreshCheckFlag: setting freshness flag', freshnessFlag
		freshFlag = freshnessFlag
		
	def getFreshFlag(self):
		global freshFlag
		global verboseMode
		if verboseMode:
			print 'CheckFreshness:getFreshFlag: getting freshness flag',freshFlag
		return freshFlag
