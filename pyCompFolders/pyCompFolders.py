#!/usr/bin/env python

# pyCompFolders.py - Compare two directory trees

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

# this class does all the work of reading a directory tree into a list
class ReadDirectoryToList:
	# browseToFolder - Opens a windows file browser to allow user to navigate to the directory to read
	# returns the file name of the path that was selected
	def browseToFolder(self):
		dialog = gtk.FileChooserDialog(title="Select folder", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		filter.set_name("Select Folder")
		filter.add_pattern("*") # what's the pattern for a folder 
		dialog.add_filter(filter)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFileName = dialog.get_filename()
			dialog.destroy()
			return(retFileName)
		elif response == gtk.RESPONSE_CANCEL: 
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
	
	# selectOutputFileName
	# returns the name of the output csv file
	def selectOutputFileName(self):
		dialog = gtk.FileChooserDialog(title="Save as", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
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
	
	# Support for drag and drop or command line execution
	# returns the path to the directory
	# if the path can't be determined returns an empty string
	def dealWithCommandLine(self):
		pathToDir = ""
		if sys.argv[0][-16:] == 'pyCompFolders.py':		# running from the command line
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
		makeDirPath = '"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /s > c:\\temp\\tempDir.txt'
		return(commandLine)
			
	# parse through the text file that was created when the directory was set up
	# returns a list of lists
	def parseDirTxt(self, filePtr, rootDirPath):
		dirFiles = []
		dirName = ""
		for textLine in filePtr:
			textLine = textLine.strip('\r\n')
			if len(textLine) == 0:
				continue
			elif " Volume in drive " in textLine:
				continue
			elif " Volume Serial Number is" in textLine:
				continue
			elif '<DIR>' in textLine:
				continue
			elif textLine.find('/') == 2:
				tempDirLine = textLine.split()
				dirLine = []
				for item in tempDirLine:
					if item != '':
						dirLine.append(item)				
				myDirFile = []
				myDirFile.append(dirLine[0])
				myDirFile.append(dirLine[1] + ' ' + dirLine[2])
				myDirFile.append(dirLine[3])
				myDirFile.append(dirLine[4])
				myDirFile.append(relDirName)
				myDirFile.append(dirName)
				dirFiles.append(myDirFile)
			elif "Directory of " in textLine:
				dirName = textLine[14:].strip()
				relDirName = dirName[len(rootDirPath):]		# relative path
			elif 'File(s)' in textLine:
				continue
			elif '     Total Files Listed:' in textLine:
				continue
			elif ' Dir(s)' in textLine:
				continue
		return(dirFiles)
		
	# deleteTempFile - delete the temporary file that was created
	def deleteTempFile(self):
		try:
			os.system('del c:\\temp\\tempDir.txt')
		except:
			print "Couldn't delete temp file"
			s = raw_input('--> ')
			exit()
	
	# doReadDir - 
	def doReadDir(self):
		pathToDir = self.dealWithCommandLine()
		if pathToDir == '':
			pathToDir = self.browseToFolder()
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
		readFile = open('c:\\temp\\tempDir.txt','rb')
		dirFileL = self.parseDirTxt(readFile, pathToDir)
		readFile.close()
		self.deleteTempFile()
		return(dirFileL)
	
	# openCSVFile - opens the CSV output file as a CSV writer output
	def openCSVFile(self, csvName):
		try:
			myCSVFile = open(csvName, 'wb')
		except:
			print "Couldn't open\nIs the file open in EXCEL?"
			s = raw_input('--> ')
			exit()
		outFil = csv.writer(myCSVFile)
		return(outFil)

myReadFolder = ReadDirectoryToList()						# create ReadDirectoryToList instance
dirFileList1 = myReadFolder.doReadDir()						# read dir structure into a list
dirFileList2 = myReadFolder.doReadDir()						# read dir structure into a list
outCSVFileName = myReadFolder.selectOutputFileName()		# get output file name
outFile = myReadFolder.openCSVFile(outCSVFileName)			# Open the output csv file

diffsList = []

# Eliminate the easy/exact matches first
for dirLineData1 in dirFileList1:								# Write out lines
	found = False
	for dirLineData2 in dirFileList2:
		if (dirLineData1[0:5] == dirLineData2[0:5]):			#date,time,size,fileName,relpath match
			found = True
	if found == False:
		outList = ['1'] + dirLineData1
		diffsList.append(outList)

for dirLineData2 in dirFileList2:								# Write out lines
	found = False
	for dirLineData1 in dirFileList1:
		if (dirLineData1[0:5] == dirLineData2[0:5]):
			found = True
	if found == False:
		outList = ['2'] + dirLineData2
		diffsList.append(outList)

outFile.writerow(['FileNum','Date','Time','Size','FileName','RelPath','AbsPath'])	# File header
for rows in diffsList:
	outFile.writerow(rows)

print 'Files : ', len(dirFileList1)
print 'Files : ', len(dirFileList2)
