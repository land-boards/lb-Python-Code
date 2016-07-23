#!/usr/bin/env python
"""
==================
dgReadDirtoList.py
==================

Methods to read a directory structure into a list and return the list.

Intended to be imported into another Python program.

==========
Background
==========

==================
Installation/Usage
==================

- Put this file into the folder C:/HWTeam/Utilities/dgCommonModules

Typical use:

- myDirReadClass = ReadDirectoryToList()	# instantiate the class
- myDirReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
- dirAsReadIn = myDirReadClass.doReadDir(defaultPath,'Select CSV File')	# read in CSV into list
- if dirAsReadIn == []:
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

sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules')

try:
	from dgProgDefaults import *
except:
	print('Need to load dgProgDefaults into C:\\HWTeam\\Utilities\\dgCommonModules')
try:
	from dgCheckFileFresh import *
except:
	print('Need to load dgCheckFileFresh into C:\\HWTeam\\Utilities\\dgCommonModules')

lastPathFileName = ''
tempFileName = ''

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

class ReadDirectoryToList:
	"""
	This class does all the work of reading a directory tree into a list of lists.
	
	Works by executing a DOS dir command. 
	Sends the output of the DOS dir command to a temporary text file.
	Parses the text file into a list.
	Returns the list.
	
	Each line in the list has:

	* 0 - Date
	* 1 - Time
	* 2 - Size
	* 3 = FileName
	* 4 - Path
	"""
	def browseToFolder(self, defaultPath,title="Select folder"):
		"""
		:return: path/filename of the selected folder
		
		Opens a windows folder browser to allow user to navigate to the folder to read.

		"""
		dialog = gtk.FileChooserDialog(title, 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		dialog.set_current_folder(defaultPath)
		filter.set_name("Select Folder")
		filter.add_pattern("*") # what's the pattern for a folder 
		dialog.add_filter(filter)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFileName = dialog.get_filename()
			dialog.destroy()
			defaultPath = retFileName
			return(retFileName)
		elif response == gtk.RESPONSE_CANCEL: 
			errorDialog('Closed, no files selected')
			dialog.destroy()
			exit()
	
	def formCommandLine(self, makeDirPath):
		"""Form the command line string to read the directory and subdirectories.

		:param makeDirPath: the path to start the dir command at
		
		:return: the command line string that does the dir command - old-skul DOS style
		
		"""
		# create a temp file name based on the datetime
		global tempFileName
		tempFileName = 'tempDir'
		tempFileName += str(int(time.time()))
		makeDirPath = '\"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /s > c:\\temp\\'
		commandLine += tempFileName
		commandLine += '.txt'
		#print 'commandLine',commandLine
		return(commandLine)
		
	def parseDirTxt(self, filePtr):
		"""
		:param filePtr: pointer to the text file that needs to be turned into a list
		:return: a list of name, date, time, size, path for each file/location
		
		Parse through the text file that was created when the directory was set up
		"""
		dirFiles = []
		dirName = ""
		global foldersList
		foldersList = []
		folderName = ""
		for textLine in filePtr:
			textLine = textLine.strip('\r\n')
			if len(textLine) == 0:
				None
			elif "Directory of " in textLine:
				dirName = textLine[14:].strip()
			elif '<DIR>' in textLine:			# add to directories list
				foldersLine = []
				foldersLine.append(textLine[0:10])
				foldersLine.append(textLine[12:20])
				foldersLine.append(textLine[39:])
				foldersList.append(foldersLine)
			elif "Volume in drive " in textLine:
				None
			elif "Volume Serial Number is" in textLine:
				None
			elif '/' in textLine:
				dirLine = []
				dirLine.append(textLine[0:10])
				dirLine.append(textLine[12:20])
				dirLine.append(textLine[22:38].strip())
				dirLine.append(textLine[39:])
				dirLine.append(dirName)
				dirFiles.append(dirLine)
			elif 'File(s)' in textLine:
				None
			elif '     Total Files Listed:' in textLine:
				None
			elif textLine.find(' Dir(s)') > 0:
				None
		return(dirFiles)
		
	def deleteTempFile(self):
		"""
		Delete the temporary file that was created.
		The temp file is located in c:\temp
		"""
		global tempFileName
		commandString = 'del c:\\temp\\'
		commandString += tempFileName
		commandString += '.txt'
		try:
			os.system(commandString)
		except:
			errorDialog("Couldn't delete temp file")
			exit()
	
	def doReadDir(self, defaultPath='',title="Select Release folder"):
		"""Read the directory into a temp file.
		Then, load the temp file into a list. 
		Then, delete the temp file.
		
		:return: the directory as a list
		
		"""		
		global lastPathFileName
		global tempFileName
		pathToDir = self.browseToFolder(defaultPath,title)
		commandString = self.formCommandLine(pathToDir)
		rval = os.system(commandString)
		if rval == 1:		# error because the c:\temp folder does not exist
			print 'Creating c:\\temp folder'
			rval2 = os.system('md c:\\temp\\')
			if rval2 == 1:
				print 'unable to create c:\\temp\\ folder'
				s = raw_input('--> ')
				exit()
			rval = os.system(commandString)
		fileNamePath = 'c:\\temp\\'
		fileNamePath += tempFileName
		fileNamePath += '.txt'
		readFile = open(fileNamePath,'rb')
		dirFileL = self.parseDirTxt(readFile)
		readFile.close()
		self.deleteTempFile()
#		print 'Release folder', pathToDir
		lastPathFileName = pathToDir
		return(dirFileL)
		
		def getFoldersList():
			return foldersList
