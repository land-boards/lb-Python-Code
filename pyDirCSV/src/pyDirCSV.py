#!/usr/bin/env python      1
"""

===========
pyDirCSV.py
===========

Read a directory structure into a CSV file

==========
Background
==========

This can be used for things like comparing two directory trees in EXCEL

==================
Installation/Usage
==================

* Browse to the folder

=========
Operation
=========

* Performs a recursive directory and dumps to a file
* Parses the directory file and puts into a list
* Turns the list into a CSV file which can be read by EXCEL

======
Output
======

Columns are:

* ['Date','Time','Size','FileName','Path']

===
API
===

"""
from __future__ import print_function

from builtins import input
from builtins import object

from tkinter import *
from tkinter import filedialog

import csv
import os
import sys

# this class does all the work of reading a directory tree into a list of lists
# each line in the list has
# 0 - Date
# 1 - Time
# 2 - Size
# 3 = FileName
# 4 - Path
class readDirectoryToList(object):
	"""Class to read a directory into a list
	"""
	def browseToFolder(self):
		"""Opens a windows file browser to allow user to navigate to the directory to read
		returns the file name of the path that was selected
		"""
		retFileName = filedialog.askdirectory()
		print ("Selected Folder: ",retFileName)
		return retFileName
	
	def dealWithCommandLine(self):
		"""

		:return: Path to the selected folder

		Support for drag and drop or command line execution.
		If the path can't be determined returns an empty string.
		"""
		pathToDir = ""
		if sys.argv[0][-11:] == 'pyDirCSV.py':		# running from the command line
			if len(sys.argv) == 2:
				pathToDir = sys.argv[1]
			elif len(sys.argv) == 1:
				None
		elif len(sys.argv) > 2:						# command line with too many passed values
			print('usage pyDirCSV path_to_search')
			s = input('--> ')
			exit()
		elif len(sys.argv) == 2:					# run from drag/drop
			pathToDir = sys.argv[0] 
		return(pathToDir)
		
	def formCommandLine(self, makeDirPath):
		"""
		:param makeDirPath: the path
		:return: the command line string

		Forms the command line string
		"""
		makeDirPath = '\"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /s > c:\\temp\\tempDir.txt'
		return(commandLine)
			
	def parseDirTxt(self, filePtr):
		"""
		:param filePtr: file handle
		:return: list of directories contents

		Parse through the text file that was created when the directory was set up
		"""
		dirFiles = []
		dirName = ""
		for textLine in filePtr:
			textLine = textLine.strip()
			if len(textLine) == 0:
				None
			elif textLine.find("Volume in drive ") != -1:
				None
			elif textLine.find("Volume Serial Number is") != -1:
				None
			elif textLine.find("Directory of ") != -1:
				dirName = textLine[14:].strip()
			elif textLine.find('<DIR>') > 0:
				None
			elif textLine.find('/') == 2:
				dirLine = []
				dirLine.append(textLine[0:10])
				dirLine.append(textLine[12:20])
				dirLine.append(textLine[22:38].strip())
				dirLine.append(textLine[39:].strip())
				dirLine.append(dirName.strip())
				dirFiles.append(dirLine)
			elif textLine.find('File(s)') > 0:
				None
			elif textLine.find('     Total Files Listed:') > 0:
				None
			elif textLine.find(' Dir(s)') > 0:
				None
		return(dirFiles)
		
	def deleteTempFile(self):
		"""Delete the temporary file that was created
		"""
		try:
			os.system('del c:\\temp\\tempDir.txt')
		except:
			print("Couldn't delete temp file")
			s = input('Hit ENTER to continue --> ')
			exit()
	
	def doReadDir(self):
		"""doReadDir - 
		"""
		pathToDir = readDirectoryToList.dealWithCommandLine(self)
		if pathToDir == '':
			pathToDir = readDirectoryToList.browseToFolder(self)
		commandString = readDirectoryToList.formCommandLine(self, pathToDir)
		rval = os.system(commandString)
		if rval == 1:		# error because the c:\temp folder does not exist
			print('Creating c:\\temp folder')
			rval2 = os.system('md c:\\temp\\')
			if rval2 == 1:
				print('unable to create c:\\temp\\ folder')
				s = input('Hit ENTER to continue --> ')
				exit()
			rval = os.system(commandString)
		readFile = open('c:\\temp\\tempDir.txt','r')
		dirFileL = readDirectoryToList.parseDirTxt(self, readFile)
		readFile.close()
		readDirectoryToList.deleteTempFile(self)
		return(dirFileL)
		
class selOutputFile(object):
	"""This class allows the user to select the output file name and opens the output file as a csv file
	"""
	def selectOutputFileName(self):
		"""
		# returns the name of the output csv file
		"""
		retFileName = filedialog.asksaveasfilename()
		return(retFileName)
	
	def openCSVFile(self, csvName):
		"""
		Opens the CSV output file as a CSV writer output
		"""
		if csvName[-4:] != '.csv' and csvName[-4:] != '.CSV':
			csvName += '.csv'
		try:
			myCSVFile = open(csvName, 'w')
		except:
			print("Couldn't open the output file. Is the file open in EXCEL?")
			s = input('Hit ENTER to exit --> ')	# wait for enter to be pressed
			exit()
		outFil = csv.writer(myCSVFile)
		return(outFil)
		
myReadFolder = readDirectoryToList()						# create readDirectoryToList instance
dirFileList = myReadFolder.doReadDir()						# read dir structure into a list

myOutFile = selOutputFile()									# create output file class
outCSVFileName = myOutFile.selectOutputFileName()			# get output file name
outFile = myOutFile.openCSVFile(outCSVFileName)				# Open the output csv file 
#write out the file header followed by the file data
outFile.writerow(['Date','Time','Size','FileName','Path'])	# File header
outFile.writerows(dirFileList)

print('Files : ', len(dirFileList))
