'''pyDups.py - Read a directory structure and check for duplicate files.
Write out a file which lists the duplicate files.
Code is written to work with Windoze dir command line output
'''

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print "PyGtk 2.3.90 or later required"
   raise SystemExit

import csv
import os
import sys
import filecmp

class readDirectoryToList:
	'''This class does all the work of reading a directory tree into a list of lists
	each line in the list has
	0 - Date
	1 - Time
	2 - Size
	3 - FileName
	4 - Path
	'''
	def browseToFolder(self):
		'''browseToFolder - Opens a windows file browser to allow user to navigate to the directory to read
		
		:returns: file name of the path that was selected
		'''
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
	
	def dealWithCommandLine(self):
		'''Support for drag and drop or command line execution
		
		:returns: the path to the directory
		If the path can't be determined returns an empty string
		'''
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
		
	def formCommandLine(self, makeDirPath):
		'''Forms the command line string
		
		:returns: command line string
		'''
		makeDirPath = '\"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /s > c:\\temp\\tempDir.txt'
		return(commandLine)
			
	def parseDirTxt(self, filePtr):
		'''Parse through the text file that was created when the directory was set up
		
		:returns: a list of lists
		'''
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
		'''delete the temporary file that was created
		'''
		try:
			os.system('del c:\\temp\\tempDir.txt')
		except:
			print "Couldn't delete temp file"
			s = raw_input('Hit ENTER to continue --> ')
			exit()
	
	def doReadDir(self):
		'''doReadDir - 
		'''
		pathToDir = readDirectoryToList.dealWithCommandLine(self)
		if pathToDir == '':
			pathToDir = readDirectoryToList.browseToFolder(self)
		commandString = readDirectoryToList.formCommandLine(self, pathToDir)
		rval = os.system(commandString)
		if rval == 1:		# error because the c:\temp folder does not exist
			print 'Creating c:\\temp folder'
			rval2 = os.system('md c:\\temp\\')
			if rval2 == 1:
				print 'unable to create c:\\temp\\ folder'
				s = raw_input('Hit ENTER to continue --> ')
				exit()
			rval = os.system(commandString)
		readFile = open('c:\\temp\\tempDir.txt','rb')
		dirFileL = readDirectoryToList.parseDirTxt(self, readFile)
		readFile.close()
		readDirectoryToList.deleteTempFile(self)
		return(dirFileL)
		
class selOutputFile:
	'''This class allows the user to select the output file name and opens the output file as a csv file
	'''
	def selectOutputFileName(self):
		'''selectOutputFileName
		
		:returns: the name of the output csv file
		'''
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
	
	def openCSVFile(self, csvName):
		"""Open the CSV file for output.
		
		:param csvName: the name of the file as a string
		"""
		try:
			myCSVFile = open(csvName, 'wb')
		except:
			print "Couldn't open\nIs the file open in EXCEL?, Try closing the file"
			s = raw_input('Hit enter to continue --> ')
			try:
				myCSVFile = open(csvName, 'wb')
			except:
				print "Couldn't open\nIs the file STILL open in EXCEL?\nExiting..."
				s = raw_input('Hit enter to exit --> ')
				exit()
		outFil = csv.writer(myCSVFile)
		return(outFil)
		
myReadFolder = readDirectoryToList()						# create readDirectoryToList instance
dirFileList = myReadFolder.doReadDir()						# read dir structure into a list

myOutFile = selOutputFile()									# create output file class
outCSVFileName = myOutFile.selectOutputFileName()			# get output file name
outFile = myOutFile.openCSVFile(outCSVFileName)				# Open the output csv file

myDelFileName = outCSVFileName[0:-4] + '_DEL.bat'
outDelFilePtr = open(myDelFileName, 'wb')


dirFileList = sorted(dirFileList, key = lambda errs: errs[2])		# sort by size
dirFileList = sorted(dirFileList, key = lambda errs: errs[3])		# sort by fileName

lastRow = ['','','','','']
outList = []
for row in dirFileList:
	if row[0:4] == lastRow[0:4]:
		pathFileNameLast = lastRow[4] +'\\' + lastRow[3]
		pathFileName = row[4] +'\\' + row[3]
		if filecmp.cmp(pathFileNameLast, pathFileName) == True:
			outList.append(lastRow)
			outList.append(row)
		else:
			print '\ndiff:'
			print row
			print lastRow
	lastRow = row

# write out the file header followed by the file data
outFile.writerow(['Date','Time','Size','FileName','Path'])	# File header
outFile.writerows(outList)

print 'Files : ', len(outList)
