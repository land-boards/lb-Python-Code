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
		else:
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
		commandLine += ' /-c /n /s > c:\\temp\\tempDir.txt'
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
				dirLine = []
#				tempDirLine = textLine.split()
#				for item in tempDirLine:
#					if item != '':
#						dirLine.append(item)
#				print 'dirLine', dirLine
				dirLine.append(textLine[0:10])
				dirLine.append(textLine[12:20])
				dirLine.append(textLine[22:38].strip())
				dirLine.append(textLine[39:].upper())
				dirLine.append(relDirName)
				dirLine.append(dirName)
				dirFiles.append(dirLine)
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
diffs1List = []
diffs2List = []

print 'Checking for complete matches date/time/size/FileName/RelativePath'
exactMatches = 0
# Eliminate the easy/exact 1-2 matches first
for dirLineData1 in dirFileList1:								# Write out lines
	diffLine1 = []
	found = False
	for dirLineData2 in dirFileList2:
		if (dirLineData1[0:5] == dirLineData2[0:5]):			#date,time,size,fileName,relpath all match
			found = True
			exactMatches += 1
	if found == False:
		diffLine1 = ['1']
		diffLine1.extend(dirLineData1)
		diffs1List.append(diffLine1)
print ' Complete matches from folder 1 to folder 2 :', exactMatches

# Eliminate the easy/exact 2-1 matches first
exactMatches = 0
for dirLineData2 in dirFileList2:								# Write out lines
	diffLine2 = []
	found = False
	for dirLineData1 in dirFileList1:
		if (dirLineData1[0:5] == dirLineData2[0:5]):
			found = True
			exactMatches += 1
	if found == False:
		diffLine2 = ['2']
		diffLine2.extend(dirLineData2)
		diffs2List.append(diffLine2)
print ' Complete matches from folder 2 to folder 1 :', exactMatches

print 'Checking for partial matches with matching relative paths'

outFile.writerow(['FileNum','Date','Time','Size','FileName','RelPath','AbsPath','Code'])	# File header

errorLines = []		# accumulate the triaged errors for printing

partMatches = 0
partDiffsFolders1 = []		# remainders
for line1 in diffs1List:
	found = False
	for line2 in diffs2List:
		if line1[3:6] == line2[3:6]:		# name, size and path match, date or time don't match
			found = True
			line1.append('Note - name/size/path match')
			errorLines.append(line1)
			partMatches += 1
			break
		elif line1[4:6] == line2[4:6]:		# name and path match, size, date, or time doesn't match
			found = True
			line1.append('Error - size mismatch')
			errorLines.append(line1)
			break
	if found == False:
		partDiffsFolders1.append(line1)
print ' Partial matches 1 to 2 (matching name/size/path/folders)', partMatches
		
partMatches = 0
partDiffsFolders2 = []
for line2 in diffs2List:
	found = False
	for line1 in diffs1List:
		if line1[3:6] == line2[3:6]:
			found = True
			line2.append('Note - name/size/path match')
			errorLines.append(line2)
			partMatches += 1
			break
		elif line1[4:6] == line2[4:6]:		# name and path match, size, date, or time doesn't match
			found = True
			line2.append('Error - size mismatch')
			errorLines.append(line2)
			break
	if found == False:
		partDiffsFolders2.append(line2)
print ' Partial matches 2 to 1 (matching name/size/path/folders)', partMatches

print 'Checking for matches in different folders'
fileMatches = 0
for line1 in partDiffsFolders1:
	found = False
	for line2 in partDiffsFolders2:
		if line1[1:5] == line2[1:5]:
			found = True
			line1.append('Note - Date/time/size/FileName match, different folder')
			errorLines.append(line1)
			fileMatches += 1
			break
		elif line1[3:5] == line2[3:5]:
			found = True
			line1.append('Note - Size/FileName match, different date/time/folder')
			errorLines.append(line1)
			fileMatches += 1
			break
		elif line1[4] == line2[4]:
			found = True
			line1.append('Error - FileName match, different date/time/size/folder')
			errorLines.append(line1)
			break
	if not found:
		line1.append('Error - Missing file')
		errorLines.append(line1)
print ' Matches in different folders 1 to 2', fileMatches

fileMatches = 0
for line2 in partDiffsFolders2:
	found = False
	for line1 in partDiffsFolders1:
		if line1[1:5] == line2[1:5]:
			found = True
			line2.append('Note - Date/time/size/FileName match, different folder')
			errorLines.append(line2)
			break
		elif line1[3:5] == line2[3:5]:
			found = True
			line2.append('Note - Size/FileName match, different date/time/folder')
			errorLines.append(line2)
			fileMatches += 1
			break
		elif line1[4] == line2[4]:
			found = True
			line2.append('Error - FileName match, different date/time/size/folder')
			errorLines.append(line2)
			break
	if not found:
		line2.append('Error - Missing file')
		errorLines.append(line2)
print ' Matches in different folders 2 to 1', fileMatches

errorLines = sorted(errorLines, key = lambda errs: errs[5])
errorLines = sorted(errorLines, key = lambda errs: errs[4])

for rows in errorLines:
	outFile.writerow(rows)

print 'Files : ', len(dirFileList1)
print 'Files : ', len(dirFileList2)
