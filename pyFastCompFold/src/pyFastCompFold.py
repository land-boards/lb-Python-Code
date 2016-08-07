"""Compares two directory trees quickly.
Allows the user to browse to the two folders and create a comparison list.

=====
Usage
=====

Program is run by either typing python pyFastCompFold.py or double clicking pyFastCompFold.py.

=============
Output Format
=============

The file output format is:

['Code','FileNum','Date','Time','Size','FileName','RelPath','AbsPath','Date*','Time*','Size*','FileName*','RelPath*','AbsPath*']

The contents of the list can vary depending upon which Code is indicated.
Also, for some codes, the fields with asterisks (*) are the matching/mismatching file.

===============
Program Options
===============

==============
Output Message
==============

There are three classes of messages:

* Errors
* Warnings
* Notes

There are a couple of Errors:

* No match for part
* Found a match for the part but it had different size

There are a couple of Warnings:

There are a couple of Notes:

============
Code follows
============

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

# global program flags
errorMsgLevel = 2	# default error message level = all messages

def errorDialog(errorString):
	"""
	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class ReadDirectoryToList:
	"""Read the directory
	this class does all the work of reading a directory tree into a list
	Includes the folder navigation and loading of the folder path
	Returns a list of lists.
	Each line has the directory elements (time, date, size, name, path).
	"""

	def __init__(self):
		return

	def browseToFolder(self, startPath):
		"""Opens a windows file browser to allow user to navigate to the directory to read
		
		:param startPath: a starting point for the path
		:returns: full pathname of the selected path
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
			retFolderName = dialog.get_filename()
			dialog.destroy()
			return(retFolderName)
		elif response == gtk.RESPONSE_CANCEL: 
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
		else:
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
		
	def formCommandLine(self, makeDirPath):
		"""Forms the command line string.
		The function executes a standard DOS style DIR command.
		The function creates a temporary file in the temp directory.
		
		:param makeDirPath: the path that the directory is of
		:returns: the command line string
		"""
		makeDirPath = '"' + makeDirPath + '\"'		# path might have spaces, etc
		commandLine = 'dir '
		commandLine += makeDirPath
		commandLine += ' /-c /n /s > c:\\temp\\tempDir.txt'
		return(commandLine)

	def openCSVFile(self, csvName):
		"""Creates an output CSV file and has the functions to write to the CSV file
		
		:param csvName: String which has the Pathfilename of the csv file
		:returns: pointer to the output file
		"""
		try:
			myCSVFile = open(csvName, 'wb')
		except:
			errorDialog("Couldn't open the output file\nIs the file open in Excel?")
			try:
				myCSVFile = open(csvName, 'wb')
			except:
				errorDialog("Couldn't open the output file, Exiting...")
				exit()
		outFil = csv.writer(myCSVFile)
		return(outFil)
		
	def parseDirToList(self, filePtr, rootDirPath):
		"""Parses through the text file that was created when the directory was set up
		
		:param filePtr: pointer to the file
		:param rootDirPath: the root of directory path - used for relative comparisons
		:returns: list of lists representing the directory structure
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
		"""Deletes the temporary file that was created.
		"""
		try:
			os.system('del c:\\temp\\tempDir.txt')
		except:
			print "Couldn't delete the temporary file c:\\temp\\tempDir.txt"
			errorDialog("Couldn't delete the temporary file c:\\temp\\tempDir.txt")
			raise SystemExit
	
	def doReadDir(self, pathToDir):
		"""Reads the directory into the tempDir.txt file in the temp folder.
		If the method is unable to create the directly it throws up an error message and quits out.
	
		:param pathToDir: the path to the directory
		:returns: list that has the directory contents
		"""
		commandString = self.formCommandLine(pathToDir)	# form the 'dir' command string
		rval = os.system(commandString)					# issue the dir command
		if rval == 1:									# error because the c:\temp folder does not exist
			print 'Creating c:\\temp folder'			# 
			rval2 = os.system('md c:\\temp\\')
			if rval2 == 1:
				errorDialog("unable to create c:\\temp\\ folder")
				raise SystemExit
			rval = os.system(commandString)
		readFile = open('c:\\temp\\tempDir.txt','rb')
		dirFileL = self.parseDirToList(readFile, pathToDir)
		readFile.close()
		self.deleteTempFile()
		return(dirFileL)
	
class SelOutFileName:
	"""Simple class to select the output filename.
	"""
	def __init__(self):
		retFolderName = ''
		return

	def selectOutputFileName(self, startPath):
		"""Select the output file name via a filechooser dialog.
		
		:returns: name of the output csv file
		"""
		dialog = gtk.FileChooserDialog(title="Save as", 
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)) 
		filter = gtk.FileFilter() 
		filter.set_name("CSV Files")
		filter.add_pattern("*.csv")
		if not startPath:
			dialog.set_current_folder(startPath)
		dialog.add_filter(filter)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFolderName = dialog.get_filename()
			dialog.destroy()
			return(retFolderName)
		elif response == gtk.RESPONSE_CANCEL: 
			print 'Closed, no files selected'
		dialog.destroy()
		exit()

class CompareTwoDirLists:
	"""Class that does the comparison of the two directory lists.
	"""
	errorLines = []					# accumulate the errors as a list for printing

	def __init__(self):
		self.errorLines = []		# accumulate the triaged errors for printing

	def detailFileComp(self, fileName1, path1, fileName2, path2):
		"""Does a very detailed file comparison of the two files.
		
		:param fileName1: The name of the first file
		:param path1: The name of the first path
		:param fileName2: The name of the second file
		:param path2: The name of the second path
		:returns: True if the files match, false if they differ
		"""
		filePath1 = ''
		filePath2 = ''
		filePath1 = path1 + '\\' + fileName1
		filePath2 = path2 + '\\' + fileName2
		return (filecmp.cmp(filePath1, filePath2))

	def addToErrorLines(self,inFileNum, errorLevel, errorString, line1String, line2String):
		"""Adds the error to the errorLines list if the error exceeds the current message level option setting.
		errorMsgLevel
		
		* 0 = report errors only
		* 1 = report errors/warnings
		* 2 = report errors/warnings/notes
		
		:param inFileNum: number which indicates which file is being referenced by the error
		:param errorLevel: The error level of this issue
		
		* 0 = errors only
		* 1 = warnings
		* 2 - note
		
		:param errorString: the string to print which describes the error
		:param line1String: the actual directory line
		:param line2String: optional other directory line
		"""

		global errorMsgLevel
		thisErrorLine = []
		thisErrorLine.append(errorString)
		thisErrorLine.append(str(inFileNum))
		thisErrorLine += line1String
		thisErrorLine += line2String
		if errorLevel <= errorMsgLevel:
			self.errorLines.append(thisErrorLine)

	def writeOutHeader(self, outFilePtr):
		"""Write out the header.
	
		:param outFilePtr: points to the output file
		"""
		outFilePtr.writerow(['Code','FileNum','Date','Time','Size','FileName','RelPath','AbsPath','Date*','Time*','Size*','FileName*','RelPath*','AbsPath*'])	# File header
		
	def writeOutList(self, outFilePtr):
		"""Write out the list.
	
		:param outFilePtr: points to the output file
		"""
		for rows in self.errorLines:
			outFilePtr.writerow(rows)

	def doCompFolders(self):
		"""The executive which calls the other functions
		"""
		myReadFolder = ReadDirectoryToList()							# create ReadDirectoryToList instance
		pathToDir1 = myReadFolder.browseToFolder('')					# get first directory name from folder browser
		print 'first folder : %s' % pathToDir1
		pathToDir2 = myReadFolder.browseToFolder(pathToDir1)			# get second directory name from folder browser
		print 'second folder : %s' % pathToDir2
		myWriteFolder = SelOutFileName()
		outCSVFileName = myWriteFolder.selectOutputFileName(pathToDir1)	# get output file name from file browser
		print 'Output file : %s' % outCSVFileName

		print 'Reading in first directory to list'
		dirFileList1 = myReadFolder.doReadDir(pathToDir1)			# read dir structure into a list

		print 'Reading in second directory to list'
		dirFileList2 = myReadFolder.doReadDir(pathToDir2)			# read dir structure into a list

		outFile = myReadFolder.openCSVFile(outCSVFileName)			# Open the output csv file
		self.writeOutHeader(outFile)

		diffs1List = []
		diffs2List = []

		# sort by size then by filename so that identical files are near each other
		print 'Sorting lists'
		dirFileList1 = sorted(dirFileList1, key = lambda errs: errs[4])		# sort by Relative Path
		dirFileList1 = sorted(dirFileList1, key = lambda errs: errs[2])		# sort by size
		dirFileList1 = sorted(dirFileList1, key = lambda errs: errs[3])		# sort by filename
		dirFileList2 = sorted(dirFileList2, key = lambda errs: errs[4])		# sort by Relative Path
		dirFileList2 = sorted(dirFileList2, key = lambda errs: errs[2])		# sort by size
		dirFileList2 = sorted(dirFileList2, key = lambda errs: errs[3])		# sort by filename

		print 'Line count in first list :', len(dirFileList1)
		print 'Line count in second list :', len(dirFileList2)
		print 'Checking for matches'
		
		lastInList1 = len(dirFileList1) - 1
		lastInList2 = len(dirFileList2) - 1
		list1Off = 0
		list2Off = 0
		printedLast1 = False
		printedLast2 = False
		reachedEnd = False
		previousLine1 = ['Date','Time','Size','FileName','RelPath','AbsPath']
		previousLine2 = ['Date','Time','Size','FileName','RelPath','AbsPath']
		while (not printedLast1) or (not printedLast2) or (not reachedEnd):
			if (dirFileList1[list1Off][3] == previousLine1[3]) and not printedLast1:
				self.addToErrorLines(1, 1, 'Warning - Duplicated file', dirFileList1[list1Off], previousLine1)
				if list1Off < lastInList1:
					previousLine1 = dirFileList1[list1Off]
					list1Off += 1
				else:
					printedLast1 = True
			elif (dirFileList2[list2Off][3] == previousLine2[3]) and not printedLast2:
				self.addToErrorLines(2, 1, 'Warning - Duplicated file', dirFileList2[list2Off], previousLine2)
				if list2Off < lastInList2:
					previousLine2 = dirFileList2[list2Off]
					list2Off += 1
				else:
					printedLast2 = True
			elif dirFileList1[list1Off][0:5] == dirFileList2[list2Off][0:5]:	# match 'Date','Time','Size','FileName',"RelPath'
				if not printedLast1:
					self.addToErrorLines(1, 2, 'Note - matching date*time*size*filename*RelPath', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						previousLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					thisErrorLine = []
					self.addToErrorLines(2, 2, 'Note - matching date*time*size*filename*RelPath', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						previousLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
			elif dirFileList1[list1Off][0:4] == dirFileList2[list2Off][0:4]:	# match 'Date','Time','Size','FileName'
				if not printedLast1:
					self.addToErrorLines(1, 2, 'Note - matching date*time*size*filename', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						previousLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					self.addToErrorLines(2, 2, 'Note - matching date*time*size*filename', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						previousLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
			elif dirFileList1[list1Off][2:4] == dirFileList2[list2Off][2:4]:	# match 'Size','FileName'
				if self.detailFileComp(dirFileList1[list1Off][3], dirFileList1[list1Off][5], dirFileList2[list2Off][3], dirFileList2[list2Off][5]) == True:
					if not printedLast1:
						self.addToErrorLines(1, 2, 'Note - matching size*filename*contents, different date|time', dirFileList1[list1Off], [''])
						if list1Off < lastInList1:
							previousLine1 = dirFileList1[list1Off]
							list1Off += 1
						else:
							printedLast1 = True
					if not printedLast2:
						self.addToErrorLines(2, 2, 'Note - matching size*filename*contents, different date|time', dirFileList2[list2Off], [''])
						if list2Off < lastInList2:
							previousLine2 = dirFileList2[list2Off]
							list2Off += 1
						else:
							printedLast2 = True
				else:
					if not printedLast1:
						self.addToErrorLines(1, 0, 'Error - matching size*filename, different contents*(date|time)', dirFileList1[list1Off], [''])
						if list1Off < lastInList1:
							previousLine1 = dirFileList1[list1Off]
							list1Off += 1
						else:
							printedLast1 = True
					if not printedLast2:
						self.addToErrorLines(2, 0, 'Error - matching size*filename, different contents*(date|time)', dirFileList2[list2Off], [''])
						if list2Off < lastInList2:
							previousLine2 = dirFileList2[list2Off]
							list2Off += 1
						else:
							printedLast2 = True
			elif dirFileList1[list1Off][3] == dirFileList2[list2Off][3]:		# match 'FileName'
				if not printedLast1:
					self.addToErrorLines(1, 0, 'Error - matching filename, different size*(date|time)', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						previousLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					self.addToErrorLines(2, 0, 'Error - matching filename, different size*(date|time)', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						previousLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
			elif dirFileList1[list1Off][2] == dirFileList2[list2Off][2]:		# match 'Size' only
				if self.detailFileComp(dirFileList1[list1Off][3], dirFileList1[list1Off][5], dirFileList2[list2Off][3], dirFileList2[list2Off][5]) == True:
					if not printedLast1:
						self.addToErrorLines(1, 2, 'Note - matching size*contents, different filename*(date|time)', dirFileList1[list1Off], [''])
						if list1Off < lastInList1:
							previousLine1 = dirFileList1[list1Off]
							list1Off += 1
						else:
							printedLast1 = True
					if not printedLast2:
						self.addToErrorLines(2, 2, 'Note - matching size*contents, different filename*(date|time)', dirFileList2[list2Off], [''])
						if list2Off < lastInList2:
							previousLine2 = dirFileList2[list2Off]
							list2Off += 1
						else:
							printedLast2 = True
				else:
					if not printedLast1:
						self.addToErrorLines(1, 2, 'Note - matching size*contents, different filename*(date|time)', dirFileList1[list1Off], [''])
						if list1Off < lastInList1:
							previousLine1 = dirFileList1[list1Off]
							list1Off += 1
						else:
							printedLast1 = True
					if not printedLast2:
						self.addToErrorLines(2, 0, 'Error - matching size, different filename*contents*(date|time)', dirFileList2[list2Off], [''])
						if list2Off < lastInList2:
							previousLine2 = dirFileList2[list2Off]
							list2Off += 1
						else:
							printedLast2 = True
			elif dirFileList1[list1Off][3] < dirFileList2[list2Off][3]:		# doesn't match 'FileName'
				if not printedLast1:
					self.addToErrorLines(1, 0, 'Error - no match for part', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						previousLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				elif not printedLast2:
					self.addToErrorLines(2, 0, 'Error - no match for part', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						previousLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
					
			elif dirFileList1[list1Off][3] > dirFileList2[list2Off][3]:		# doesn't match 'FileName'
				if not printedLast2:
					self.addToErrorLines(2, 0, 'Error - no match for part', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						previousLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
				elif not printedLast1:
					self.addToErrorLines(1, 0, 'Error - no match for part', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						previousLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
			if printedLast1 and printedLast2:
				reachedEnd = True

		self.errorLines = sorted(self.errorLines, key = lambda errs: errs[1])
		self.errorLines = sorted(self.errorLines, key = lambda errs: errs[5])
		
		self.writeOutList(outFile)

class UIManager:
	interface = """
	<ui>
		<menubar name="MenuBar">
			<menu action="File">
				<menuitem action="Open"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="Options">
				<menuitem action="ErrorsOnly"/>
				<menuitem action="ErrorsAndWarns"/>
				<menuitem action="AllMessages"/>
			</menu>
			<menu action="Help">
				<menuitem action="About"/>
			</menu>
		</menubar>
	</ui>
	"""

	def __init__(self):
		# Create the top level window
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
		actiongroup =  gtk.ActionGroup("pyFastCompFold")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
			("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
			("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
			("File", None, "_File"),
			("Options", None, "_Options"),
			("Help", None, "_Help"),
			("About", None, "_About", None, "About pyFastCompFold", self.about_pycompfolders),
			])
		self.actiongroup.add_radio_actions([
			("ErrorsOnly", gtk.STOCK_PREFERENCES, "_Report Errors Only", '<Control>E', "Only save errors", 0),
			("ErrorsAndWarns", gtk.STOCK_PREFERENCES, "_Report Errors/Warnings", '<Control>W', "Save errors and warnings", 1),
			("AllMessages", gtk.STOCK_PREFERENCES, "_Report All Messages", '<Control>A', "Save all messages", 2),
			], 2, self.setErrorMsgLevel)
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		compFold = CompareTwoDirLists()
		compFold.doCompFolders()
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("Comparison Completed")
		message.run()
		message.destroy()

		return

	def about_pycompfolders(self, b):
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyFastCompFold\nAuthor: Doug Gilliland\n(c) 2014 - AAC - All rights reserved\npyFastCompFold compares two folders and lists the differences")
		message.run()
		message.destroy()
		
	def setErrorMsgLevel(self, action, current):
		global errorMsgLevel
		text = current.get_name()
		if (text == "ErrorsOnly"):
			errorMsgLevel = 0
			print 'Report Errors Only'
		elif (text == "ErrorsAndWarns"):
			errorMsgLevel = 1
			print 'Report Error and Warning messages'
		elif (text == "AllMessages"):
			errorMsgLevel = 2
			print 'Report Errors, Warnings and Notes'
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
