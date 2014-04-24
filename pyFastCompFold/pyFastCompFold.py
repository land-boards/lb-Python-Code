# pyFastCompFold.py - Compare two directory trees

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
folderStrucChangesFlag = 0
errorMsgLevel = 2

# this class does all the work of reading a directory tree into a list
# Includes the folder navigation and loading of the folder path
# Returns a list of lists.
# Each line has the directory elements (time, date, size, name, path).
class ReadDirectoryToList:
	# browseToFolder - Opens a windows file browser to allow user to navigate to the directory to read
	# returns the file name of the path that was selected
	def browseToFolder(self, startPath):
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
	def doReadDir(self, pathToDir):
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
	# selectOutputFileName
	# returns the name of the output csv file
	def selectOutputFileName(self, startPath):
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

def detailFileComp(fileName1, path1, fileName2, path2):
	filePath1 = ''
	filePath2 = ''
	filePath1 = path1 + '\\' + fileName1
	filePath2 = path2 + '\\' + fileName2
	return (filecmp.cmp(filePath1, filePath2))

errorLines = []		# accumulate the triaged errors for printing

# errorMsgLevel
# 0 = report errors only
# 1 = report errors/warnings
# 2 = report errors/warnings/notes
#
# Passed 
# inFileNum - number which indicates which file is being referenced by the error
# errorLevel - 
# 0 = errors only
# 1 = warnings
# 2 - note
# errorString - the string to print which describes the error
# line1String - the actual directory line
# line2String - optional other directory line
#
# replaces these 7 lines of code - 
# thisErrorLine = []
# thisErrorLine.append('Warning - Duplicated file')
# thisErrorLine.append('1')
# thisErrorLine += dirFileList1[list1Off]
# thisErrorLine += lastLine1
# if errorMsgLevel > 0:
#	errorLines.append(thisErrorLine)
# replace with this line -
# addToErrorLines(1, 'Warning - Duplicated file', 1, dirFileList1[list1Off], lastLine1)
def addToErrorLines(inFileNum, errorLevel, errorString, line1String, line2String):
	global errorLines
	thisErrorLine = []
	thisErrorLine.append(errorString)
	thisErrorLine.append(str(inFileNum))
	thisErrorLine += line1String
	thisErrorLine += line2String
	if errorLevel <= errorMsgLevel:
		errorLines.append(thisErrorLine)

def doCompFolders():
	global errorLines
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

	outFile.writerow(['Code','FileNum','Date','Time','Size','FileName','RelPath','AbsPath','Date*','Time*','Size*','FileName*','RelPath*','AbsPath*'])	# File header

	print 'Checking for matches'
	
	lastInList1 = len(dirFileList1) - 1
	lastInList2 = len(dirFileList2) - 1
	list1Off = 0
	list2Off = 0
	printedLast1 = False
	printedLast2 = False
	reachedEnd = False
	lastLine1 = ['Date','Time','Size','FileName','RelPath','AbsPath']
	lastLine2 = ['Date','Time','Size','FileName','RelPath','AbsPath']
	while 1:
#		print 'comparing (1) %s to (2) %s' % (dirFileList1[list1Off][3], dirFileList2[list2Off][3])
		if (dirFileList1[list1Off][3] == lastLine1[3]) and not printedLast1:
			addToErrorLines(1, 1, 'Warning - Duplicated file', dirFileList1[list1Off], lastLine1)
			if list1Off < lastInList1:
				lastLine1 = dirFileList1[list1Off]
				list1Off += 1
			else:
				printedLast1 = True
		elif (dirFileList2[list2Off][3] == lastLine2[3]) and not printedLast2:
			addToErrorLines(2, 1, 'Warning - Duplicated file', dirFileList2[list2Off], lastLine2)
			if list2Off < lastInList2:
				lastLine2 = dirFileList2[list2Off]
				list2Off += 1
			else:
				printedLast2 = True
		elif dirFileList1[list1Off][0:5] == dirFileList2[list2Off][0:5]:	# match 'Date','Time','Size','FileName',"RelPath'
			if not printedLast1:
				addToErrorLines(1, 2, 'Note - matching date*time*size*filename*RelPath', dirFileList1[list1Off], [''])
				if list1Off < lastInList1:
					lastLine1 = dirFileList1[list1Off]
					list1Off += 1
				else:
					printedLast1 = True
			if not printedLast2:
				thisErrorLine = []
				addToErrorLines(2, 2, 'Note - matching date*time*size*filename*RelPath', dirFileList2[list2Off], [''])
				if list2Off < lastInList2:
					lastLine2 = dirFileList2[list2Off]
					list2Off += 1
				else:
					printedLast2 = True
		elif dirFileList1[list1Off][0:4] == dirFileList2[list2Off][0:4]:	# match 'Date','Time','Size','FileName'
			if not printedLast1:
				addToErrorLines(1, 2, 'Note - matching date*time*size*filename', dirFileList1[list1Off], [''])
				if list1Off < lastInList1:
					lastLine1 = dirFileList1[list1Off]
					list1Off += 1
				else:
					printedLast1 = True
			if not printedLast2:
				addToErrorLines(2, 2, 'Note - matching date*time*size*filename', dirFileList2[list2Off], [''])
				if list2Off < lastInList2:
					lastLine2 = dirFileList2[list2Off]
					list2Off += 1
				else:
					printedLast2 = True
		elif dirFileList1[list1Off][2:4] == dirFileList2[list2Off][2:4]:	# match 'Size','FileName'
			if detailFileComp(dirFileList1[list1Off][3], dirFileList1[list1Off][5], dirFileList2[list2Off][3], dirFileList2[list2Off][5]) == True:
				if not printedLast1:
					addToErrorLines(1, 2, 'Note - matching size*filename*contents, different date|time', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						lastLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					addToErrorLines(2, 2, 'Note - matching size*filename*contents, different date|time', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						lastLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
			else:
				if not printedLast1:
					addToErrorLines(1, 0, 'Error - matching size*filename, different contents*(date|time)', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						lastLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					addToErrorLines(2, 0, 'Error - matching size*filename, different contents*(date|time)', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						lastLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
		elif dirFileList1[list1Off][3] == dirFileList2[list2Off][3]:		# match 'FileName'
			if not printedLast1:
				addToErrorLines(1, 0, 'Error - matching filename, different size*(date|time)', dirFileList1[list1Off], [''])
				if list1Off < lastInList1:
					lastLine1 = dirFileList1[list1Off]
					list1Off += 1
				else:
					printedLast1 = True
			if not printedLast2:
				addToErrorLines(2, 0, 'Error - matching filename, different size*(date|time)', dirFileList2[list2Off], [''])
				if list2Off < lastInList2:
					lastLine2 = dirFileList2[list2Off]
					list2Off += 1
				else:
					printedLast2 = True
		elif dirFileList1[list1Off][2] == dirFileList2[list2Off][2]:		# match 'Size' only
			if detailFileComp(dirFileList1[list1Off][3], dirFileList1[list1Off][5], dirFileList2[list2Off][3], dirFileList2[list2Off][5]) == True:
				if not printedLast1:
					addToErrorLines(1, 2, 'Note - matching size*contents, different filename*(date|time)', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						lastLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					addToErrorLines(2, 2, 'Note - matching size*contents, different filename*(date|time)', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						lastLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
			else:
				if not printedLast1:
					addToErrorLines(1, 0, 'Note - matching size*contents, different filename*(date|time)', dirFileList1[list1Off], [''])
					if list1Off < lastInList1:
						lastLine1 = dirFileList1[list1Off]
						list1Off += 1
					else:
						printedLast1 = True
				if not printedLast2:
					addToErrorLines(2, 0, 'Error - matching size, different filename*contents*(date|time)', dirFileList2[list2Off], [''])
					if list2Off < lastInList2:
						lastLine2 = dirFileList2[list2Off]
						list2Off += 1
					else:
						printedLast2 = True
		elif dirFileList1[list1Off][3] < dirFileList2[list2Off][3]:		# doesn't match 'FileName'
			if not printedLast1:
				addToErrorLines(1, 0, 'Error - no match for part', dirFileList1[list1Off], [''])
				if list1Off < lastInList1:
					lastLine1 = dirFileList1[list1Off]
					list1Off += 1
				else:
					printedLast1 = True
			elif not printedLast2:
				addToErrorLines(2, 0, 'Error - no match for part', dirFileList2[list2Off], [''])
				if list2Off < lastInList2:
					lastLine2 = dirFileList2[list2Off]
					list2Off += 1
				else:
					printedLast2 = True
				
		elif dirFileList1[list1Off][3] > dirFileList2[list2Off][3]:		# doesn't match 'FileName'
			if not printedLast2:
				addToErrorLines(2, 0, 'Error - no match for part', dirFileList2[list2Off], [''])
				if list2Off < lastInList2:
					lastLine2 = dirFileList2[list2Off]
					list2Off += 1
				else:
					printedLast2 = True
			elif not printedLast1:
				addToErrorLines(1, 0, 'Error - no match for part', dirFileList1[list1Off], [''])
				if list1Off < lastInList1:
					lastLine1 = dirFileList1[list1Off]
					list1Off += 1
				else:
					printedLast1 = True

		if printedLast1 and printedLast2 and reachedEnd:
			break
		elif printedLast1 and printedLast2:
			reachedEnd = True

	errorLines = sorted(errorLines, key = lambda errs: errs[1])
	errorLines = sorted(errorLines, key = lambda errs: errs[5])

	for rows in errorLines:
		outFile.writerow(rows)

	print 'Files :', len(dirFileList1)
	print 'Files :', len(dirFileList2)


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
			], 2, self.errorMsgLevel)
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		doCompFolders()
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
		
	def errorMsgLevel(self, action, current):
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
