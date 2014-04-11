#!/usr/bin/env python

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

class readDirectoryToList:
	# browseToPath - Opens a windows file browser to allow user to navigate to the directory to read
	def browseToPath(self):
		dialog = gtk.FileChooserDialog(title="Select folder", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		filter.set_name("Select Folder")
		filter.add_pattern("*") # whats the pattern for a folder 
		dialog.add_filter(filter)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			return(dialog.get_filename())
		elif response == gtk.RESPONSE_CANCEL: 
			print 'Closed, no files selected'
		dialog.destroy()
	
	# Support for drag and drop or command line execution
	# returns the path to the directory
	# if the path can't be determined returns an empty string
	def dealWithCommandLine(self):
		pathToDir = ""
		if sys.argv[0][-11:] == 'pyDirCSV.py':		# running from the command line
			if len(sys.argv) == 2:
				pathToDir = sys.argv[1]
			elif len(sys.argv) == 1:
				None
		elif len(sys.argv) > 2:						# command line with too many passed values
			print 'usage pyDirCSV path_to_search'
			s = raw_input('--> ')
			exit()
		elif len(sys.argv) == 2:					# run from drag/drop
			pathToDir = sys.argv[0] 
		return(pathToDir)
		
	# formCommandLine - Forms the command line string
	# returns the command line string
	def formCommandLine(self, makeDirPath):
		makeDirPath = '\"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /s > c:\\temp\\tempDir.txt'
		return(commandLine)
			
	# parse through the text file that was created when the directory was set up
	def parseDirTxt(self, filePtr):
		dirFiles = []
		dirName = ""
		for textLine in filePtr:
			textLine = textLine.strip('\r\n')
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
				dirLine.append(textLine[39:])
				dirLine.append(dirName)
				dirFiles.append(dirLine)
			elif textLine.find('File(s)') > 0:
				None
			elif textLine.find('     Total Files Listed:') > 0:
				None
			elif textLine.find(' Dir(s)') > 0:
				None
		return(dirFiles)
		
	def deleteTempFile(self):
		try:
			os.system('del c:\\temp\\tempDir.txt')
		except:
			print "Couldn't delete temp file"
			exit()
	
	def doReadDir(self):
		pathToDir = readDirectoryToList.dealWithCommandLine(self)
		if pathToDir == '':
			pathToDir = readDirectoryToList.browseToPath(self)
		commandString = readDirectoryToList.formCommandLine(self, pathToDir)
		
		rval = os.system(commandString)
		#print 'rval', rval
		if rval == 1:
			print 'Error running dir command'
			s = raw_input('--> ')
			exit()
	
		readFile = open('c:\\temp\\tempDir.txt','rb')
		dirFileList = readDirectoryToList.parseDirTxt(self, readFile)
		readFile.close()
		readDirectoryToList.deleteTempFile(self)
		return(dirFileList)

# create an instance of the readDirectoryToList class
myReadFolder = readDirectoryToList()

# read the directory structure into a list
dirFileList = myReadFolder.doReadDir()

# Open the output csv file
try:
	myCSVFile = open('c:\\temp\\results.csv', 'wb')
except:
	print "Couldn't open\nIs the file open in EXCEL?"
	exit()
# Open file as a CSV writer output
outFile = csv.writer(myCSVFile)

# Write out the file header
outFile.writerow(['Date','Time','Size','FileName','Path'])
# Write out all of the lines in the file
for dirLineData in dirFileList:
	outFile.writerow(dirLineData)

print 'Files : ', len(dirFileList)
