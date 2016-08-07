"""

================
pyCompFolders.py
================

Compare two directory trees

==========
Background
==========

==================
Installation/Usage
==================

* Browse to first folder
* Browse to second folder
* Select output folder/file name

======
Output
======

Columns are:

* Code	
* FileNum	
* Date	
* Time	
* Size	
* FileName	
* RelPath
* AbsPath	
* Date*	
* Time*	
* Size*	
* FileName*	
* RelPath*	
* AbsPath*

===
API
===

"""
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

import filecmp		# Used to compare files which have same name and size

verboseFlag = 0
folderStrucChangesFlag = 0

class ReadDirectoryToList:
	"""
	This class does all the work of reading a directory tree into a list
	Includes the folder navigation and loading of the folder path
	Returns a list of lists.
	Each line has the directory elements (time, date, size, name, path).
	"""
	def browseToFolder(self, startPath):
		"""
		
		:param startPath: Where to start searching
		:return: Path to the selected folder

		Opens a windows file browser to allow user to navigate to the directory to read
		"""
		dialog = gtk.FileChooserDialog(title="Select folder", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		filter.set_name("Select Folder")
		filter.add_pattern("*") # what's the pattern for a folder 
		dialog.add_filter(filter)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		if startPath != '':
			dialog.set_current_folder(startPath)
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
		
	def formCommandLine(self, makeDirPath):
		"""
		
		:param makeDirPath: Path to output file
		:return: The command line

		Forms the command line string.
		"""
		makeDirPath = '"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /n /s > c:\\temp\\tempDir.txt'
		return(commandLine)
			
	def parseDirTxt(self, filePtr, rootDirPath):
		"""
		
		:param filePtr: Path to directory text file
		:param rootDirPath: Path to root
		:return: list of directory contents

		parse through the text file that was created when the directory was set up
		"""
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
	
	def deleteTempFile(self):
		"""
		Delete the temporary file that was created
		"""
		try:
			os.system('del c:\\temp\\tempDir.txt')
		except:
			print "Couldn't delete temp file"
			s = raw_input('--> ')
			exit()
	
	def doReadDir(self, pathToDir):
		"""
		
		:param pathToDir: Path to directory
		:return: the directory as a list

		"""
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
	
	def openCSVFile(self, csvName):
		"""
		
		:param csvName: Path file name
		:return: file handle

		Opens the CSV output file as a CSV writer output
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
		
class WriteDirectoryCSV:
	def selectOutputFileName(self, startPath):
		"""
		
		:param startPath: Path file name
		:return: name of the output csv file
		
		"""
		dialog = gtk.FileChooserDialog(title="Save as", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		filter.set_name("*.csv")
		filter.add_pattern("*.csv") # whats the pattern for a folder 
		if startPath != '':
			dialog.set_current_folder(startPath)
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

def doCompFolders():
	"""
	
	Commpare folders method
	"""
	myReadFolder = ReadDirectoryToList()							# create ReadDirectoryToList instance
	pathToDir1 = myReadFolder.browseToFolder('')					# get first directory name from folder browser
	print 'first folder : %s' % pathToDir1
	pathToDir2 = myReadFolder.browseToFolder(pathToDir1)			# get second directory name from folder browser
	print 'second folder : %s' % pathToDir2
	myWriteFolder = WriteDirectoryCSV()
	outCSVFileName = myWriteFolder.selectOutputFileName(pathToDir1)	# get output file name from file browser
	print 'Output file : %s' % outCSVFileName

	print 'Reading in first directory to list'
	dirFileList1 = myReadFolder.doReadDir(pathToDir1)			# read dir structure into a list

	print 'Reading in second directory to list'
	dirFileList2 = myReadFolder.doReadDir(pathToDir2)			# read dir structure into a list

	outFile = myReadFolder.openCSVFile(outCSVFileName)			# Open the output csv file

	diffs1List = []
	diffs2List = []
	errorLines = []		# accumulate the triaged errors for printing

	print 'Sorting lists'
	dirFileList1 = sorted(dirFileList1, key = lambda errs: errs[2])
	dirFileList1 = sorted(dirFileList1, key = lambda errs: errs[3])
	dirFileList2 = sorted(dirFileList2, key = lambda errs: errs[2])
	dirFileList2 = sorted(dirFileList2, key = lambda errs: errs[3])
	
	print 'Line count in first list :', len(dirFileList1)
	print 'Line count in second list :', len(dirFileList2)

	outFile.writerow(['Code','FileNum','Date','Time','Size','FileName','RelPath','AbsPath','Date*','Time*','Size*','FileName*','RelPath*','AbsPath*'])	# File header

	#################################################
	# Check for EXACT matches
	# Date,Time,Size,FileName,RelPath

	if folderStrucChangesFlag == 1:
		print 'Checking for complete matches date/time/size/FileName/RelativePath'
		exactMatches = 0
		# Eliminate the easy/exact 1-2 matches first
		for dirLineData1 in dirFileList1:								# Write out lines
			found = False
			for dirLineData2 in dirFileList2:
				if (dirLineData1[0:5] == dirLineData2[0:5]):			#date,time,size,fileName,relpath all match
					found = True
					exactMatches += 1
			if found == False:
				diffs1List.append(dirLineData1)
		print ' Complete matches from RelFolder 1 to RelFolder 2 :', exactMatches

		# Eliminate the easy/exact 2-1 matches first
		exactMatches = 0
		for dirLineData2 in dirFileList2:								# Write out lines
			found = False
			for dirLineData1 in dirFileList1:
				if (dirLineData1[0:5] == dirLineData2[0:5]):
					found = True
					exactMatches += 1
			if found == False:
				diffs2List.append(dirLineData2)
		print ' Complete matches from RelFolder 2 to RelFolder 1 :', exactMatches


		#################################################
		# Check for partial matches
		# Date,Time,Size,FileName,RelPath

		print 'Checking for partial matches with matching relative paths'
		partMatches = 0
		partDiffsFolders1 = []		# remainders
		for line1 in diffs1List:
			found = False
			for line2 in diffs2List:
				if line1[2:5] == line2[2:5]:		# size, name, and relpath match, date or time don't match
					found = True
					thisErrorLine = []
					thisErrorLine.append('Note - Size/Name/RelPath match')
					thisErrorLine.append('1')
					thisErrorLine += line1
					errorLines.append(thisErrorLine)
					partMatches += 1
					break
				elif line1[3:5] == line2[3:5]:		# name and pathrel match, size, date, or time doesn't match
					found = True
					thisErrorLine = []
					thisErrorLine.append('Error - Name/RelPath match, size/date/time mismatch')
					thisErrorLine.append('1')
					thisErrorLine += line1
					errorLines.append(thisErrorLine)
					partMatches += 1
					break
			if found == False:
				partDiffsFolders1.append(line1)
		print ' Partial matches 1 to 2 (matching name/size/path/folders) :', partMatches

		partMatches = 0
		partDiffsFolders2 = []
		for line2 in diffs2List:
			found = False
			for line1 in diffs1List:
				if line1[2:5] == line2[2:5]:
					found = True
					thisErrorLine = []
					thisErrorLine.append('Note - Size/Name/RelPath match')
					thisErrorLine.append('2')
					thisErrorLine += line2
					errorLines.append(thisErrorLine)
					partMatches += 1
					break
				elif line1[3:5] == line2[3:5]:		# name and path match, size, date, or time doesn't match
					found = True
					thisErrorLine = []
					thisErrorLine.append('Error - Name/RelPath match, size/date/time mismatch')
					thisErrorLine.append('2')
					thisErrorLine += line2
					errorLines.append(thisErrorLine)
					partMatches += 1
					break
			if found == False:
				partDiffsFolders2.append(line2)
		print ' Partial matches 2 to 1 (matching name/size/path/folders) :', partMatches
	else:
		partDiffsFolders1 = dirFileList1
		partDiffsFolders2 = dirFileList2
		
	print 'Checking for matches in different folders'
	fileMatches = 0
	for line1 in partDiffsFolders1:
		found = False
		for line2 in partDiffsFolders2:
			if line1[0:4] == line2[0:4]:
				found = True
				thisErrorLine = []
				thisErrorLine.append('Note - Date*time*size*name match, different RelPath')
				thisErrorLine.append('1')
				thisErrorLine += line1
				errorLines.append(thisErrorLine)
				fileMatches += 1
				if not verboseFlag:
					break
			elif line1[2:4] == line2[2:4]:	# Size/FileName match, different date/time/folder
				found = True
				thisErrorLine = []
				filePath1 = ''
				filePath2 = ''
				filePath1 = line1[5] + '\\' + line1[3]
				filePath2 = line2[5] + '\\' + line2[3]
				if filecmp.cmp(filePath1, filePath2) == True:
					thisErrorLine.append('Note - Size*FileName*contents match, different RelPath*(date|time)')
					print '+',
				else:
					thisErrorLine.append('Error - Size*FileName match, different RelPath*contents*(date|time)')
					print '-',
				thisErrorLine.append('1')
				thisErrorLine += line1
				errorLines.append(thisErrorLine)
				fileMatches += 1
				if not verboseFlag:
					break
			elif line1[3] == line2[3]:		# File name match, other stuff maybe not
				found = True
				thisErrorLine = []
				thisErrorLine.append('Error - FileName match, different RelPath*size*(date|time)')
				thisErrorLine.append('1')
				thisErrorLine += line1
				errorLines.append(thisErrorLine)
				if not verboseFlag:
					break
			elif line1[0:3] == line2[0:3]:		# date/time/size match, filename mismatch
				thisErrorLine = []
				filePath1 = ''
				filePath2 = ''
				filePath1 = line1[5] + '\\' + line1[3]
				filePath2 = line2[5] + '\\' + line2[3]
				if filecmp.cmp(filePath1, filePath2) == True:
					found = True
					thisErrorLine.append('Note - Date*time*size*contents match, different name|RelPath')
					thisErrorLine.append('1')
					print '+',
					thisErrorLine += line1
					thisErrorLine += line2
					errorLines.append(thisErrorLine)
					if not verboseFlag:
						break
			elif line1[2] == line2[2]:		# size match, name*date|time mismatch
				thisErrorLine = []
				filePath1 = ''
				filePath2 = ''
				filePath1 = line1[5] + '\\' + line1[3]
				filePath2 = line2[5] + '\\' + line2[3]
				if filecmp.cmp(filePath1, filePath2) == True:
					found = True
					thisErrorLine.append('Note - size*contents match, different RelPath*(date|time|name)')
					thisErrorLine.append('1')
					print '+',
					thisErrorLine += line1
					thisErrorLine += line2
					errorLines.append(thisErrorLine)
					if not verboseFlag:
						break
		if not found:
			thisErrorLine = []
			thisErrorLine.append('Error - Missing file')
			thisErrorLine.append('1')
			thisErrorLine += line1
			errorLines.append(thisErrorLine)
	print '\n Matches in different folders 1 to 2 :', fileMatches

	fileMatches = 0
	for line2 in partDiffsFolders2:
		found = False
		for line1 in partDiffsFolders1:
			if line1[0:4] == line2[0:4]:
				found = True
				thisErrorLine = []
				thisErrorLine.append('Note - Date*time*size*name match, different RelPath')
				thisErrorLine.append('2')
				thisErrorLine += line2
				errorLines.append(thisErrorLine)
				fileMatches += 1
				if not verboseFlag:
					break
			elif line1[2:4] == line2[2:4]:	# Size/FileName match, different date/time/folder
				found = True
				thisErrorLine = []
				filePath1 = ''
				filePath2 = ''
				filePath1 = line1[5] + '\\' + line1[3]
				filePath2 = line2[5] + '\\' + line2[3]
				if filecmp.cmp(filePath1, filePath2) == True:
					thisErrorLine.append('Note - Size*FileName*contents match, different RelPath*(date|time)')
					print '+',
				else:
					thisErrorLine.append('Error - Size*FileName match, different RelPath*contents*(date|time)')
					print '-',
				thisErrorLine.append('2')
				thisErrorLine += line2
				errorLines.append(thisErrorLine)
				fileMatches += 1
				if not verboseFlag:
					break
			elif line1[3] == line2[3]:
				found = True
				thisErrorLine = []
				thisErrorLine.append('Error - FileName match, different RelPath*size*(date|time)')
				thisErrorLine.append('2')
				thisErrorLine += line2
				errorLines.append(thisErrorLine)
				if not verboseFlag:
					break
			elif line1[0:3] == line2[0:3]:		# date/time/size match, filename mismatch
				thisErrorLine = []
				filePath1 = ''
				filePath2 = ''
				filePath1 = line1[5] + '\\' + line1[3]
				filePath2 = line2[5] + '\\' + line2[3]
				if filecmp.cmp(filePath1, filePath2) == True:
					found = True
					thisErrorLine.append('Note - Date*time*size*contents match, different name|RelPath')
					thisErrorLine.append('2')
					print '+',
					thisErrorLine += line2
					thisErrorLine += line1
					errorLines.append(thisErrorLine)
					if not verboseFlag:
						break
			elif line1[2] == line2[2]:		# size match, name*date|time mismatch
				thisErrorLine = []
				filePath1 = ''
				filePath2 = ''
				filePath1 = line1[5] + '\\' + line1[3]
				filePath2 = line2[5] + '\\' + line2[3]
				if filecmp.cmp(filePath1, filePath2) == True:
					found = True
					thisErrorLine.append('Note - size*contents match, different RelPath*(date|time|name)')
					thisErrorLine.append('2')
					print '+',
					thisErrorLine += line2
					thisErrorLine += line1
					errorLines.append(thisErrorLine)
					if not verboseFlag:
						break
		if not found:
			thisErrorLine = []
			thisErrorLine.append('Error - Missing file')
			thisErrorLine.append('2')
			thisErrorLine += line2
			errorLines.append(thisErrorLine)
	print '\n Matches in different folders 2 to 1 :', fileMatches

	errorLines = sorted(errorLines, key = lambda errs: errs[1])
	errorLines = sorted(errorLines, key = lambda errs: errs[5])

	for rows in errorLines:
		outFile.writerow(rows)

	print 'Files :', len(dirFileList1)
	print 'Files :', len(dirFileList2)


class UIManager:
	"""The User Interface - GTK based
	"""
	interface = """
	<ui>
		<menubar name="MenuBar">
			<menu action="File">
				<menuitem action="Open"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="Options">
				<menuitem action="Verbose"/>
				<menuitem action="First"/>
				 <separator />
				<menuitem action="StrucFold"/>
				<menuitem action="UnstrucFold"/>
			</menu>
			<menu action="Help">
				<menuitem action="About"/>
			</menu>
		</menubar>
	</ui>
	"""

	def __init__(self):
		"""
		Create the top level window
		"""
		window = gtk.Window()
		window.connect('destroy', lambda w: gtk.main_quit())
		window.set_default_size(200, 200)
		
		vbox = gtk.VBox()
		
		# Create a UIManager instance
		uimanager = gtk.UIManager()

		# Add the accelerator group to the toplevel window
		accelgroup = uimanager.get_accel_group()
		window.add_accel_group(accelgroup)

		# Create an ActionGroup
		actiongroup =  gtk.ActionGroup("pyCompBom")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
			("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
			("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
			("File", None, "_File"),
			("Options", None, "_Options"),
			("Help", None, "_Help"),
			("About", None, "_About", None, "About pyCompFolders", self.about_pycompfolders),
			])
		self.actiongroup.add_radio_actions([
			("Verbose", gtk.STOCK_PREFERENCES, "_Verbose", '<Control>V', "Verbose - check all the list", 0),
			("First", gtk.STOCK_PREFERENCES, "_First", '<Control>F', "First - scan list till first message", 1),
			], 1, self.verboseSingle)
		self.actiongroup.add_radio_actions([
			("StrucFold", gtk.STOCK_PREFERENCES, "_StrucFold", '<Control>S', "Check Folder Structure", 0),
			("UnstrucFold", gtk.STOCK_PREFERENCES, "_UnstrucFold", '<Control>U', "Do not check Folder Structure", 1),
			], 1, self.folderStrucChange)
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		"""Single interface
		"""
		doCompFolders()
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("Comparison Completed")
		message.run()
		message.destroy()

		return

	def about_pycompfolders(self, b):
		"""About message
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyCompFolders\nAuthor: Doug Gilliland\n(c) 2016 - AAC - All rights reserved\npyCompFolders compares two folders and lists the differences")
		message.run()
		message.destroy()
		
	def folderStrucChange(self, action, current):
		"""Set folder structure change flag
		"""
		global folderStrucChangesFlag
		text = current.get_name()
		if (text == "StrucFold"):
			folderStrucChangesFlag = 1
			print 'Check folder structure'
		elif (text == "UnstrucFold"):
			folderStrucChangesFlag = 0
			print "Don't check folder structure"
		return
		
	def verboseSingle(self, action, current):
		"""Set verbose
		"""
		global verboseFlag
		text = current.get_name()
		if (text == "Verbose"):
			verboseFlag = 1
			print 'Verbose mode - all messages'
		elif (text == "First"):
			verboseFlag = 0
			print 'First message occurrence mode'
		return

	def quit_application(self, widget):
		"""quit
		"""
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
