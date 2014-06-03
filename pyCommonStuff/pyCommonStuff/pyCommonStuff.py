"""Some common Python Patterns
"""

import string

class pathFileExtracts:
	"""Extract file names and path from pathfilenames
	"""
	def	extractPathFromPathfilename(self,fullPathFilename):
		"""Extract Path from fullPathFilename
		"""
		return(fullPathFilename[0:fullPathFilename.rfind('\\')+1])

	def extractFilenameFromPathfilename(self,fullPathFilename):
		"""Extract fileName without extension from pathfullPathName
		"""
		return(fullPathFilename[fullPathFilename.rfind('\\')+1:-4])

	def extractFilenameNoextFromPathfilename(self,fullPathFilename):
		"""Extract fileName from pathfullPathName
		"""
		return(fullPathFilename[fullPathFilename.rfind('\\')+1:])

	def testExtracts(self):
		"""Test Code
		"""
		testFullpathFilename = 'c:\\mypath\doug.csv'

		print extractPathFromPathfilename(testFullpathFilename)
		print extractFilenameFromPathfilename(testFullpathFilename)
		print extractFilenameNoextFromPathfilename(testFullpathFilename)

"""reading in an XML file
"""

# Use the ElementTree module but alias it as "Xml"
import xml.etree.ElementTree as Xml

class XMLtoList:
	"""XMLtoList class reads the XML file into a list
	"""
	def readSpreadsheetXML2List(self, inFileN):
		"""returns list which contains the XML spreadsheet data
		"""
		# Get the root by parsing the XML file and then using the "getroot" method 
		root = Xml.parse(inFileN).getroot()

		# Get the worksheet section by findall all of the worksheet tags (should only be one) then selecting the first 
		worksheet = root.findall("{urn:schemas-microsoft-com:office:spreadsheet}Worksheet")[0]

		# Get the table section
		table = worksheet.findall('{urn:schemas-microsoft-com:office:spreadsheet}Table')[0]

		# Make a new list to store the data read from the cells 
		xmlData = []

		# Loop through all the elements directly under the table 
		for row in table.findall("{urn:schemas-microsoft-com:office:spreadsheet}Row"):
			new_list = []			# Append a new list onto the results to store that row's data
			xmlData.append(new_list)
			for cell in row:		# Loop through all the cells in the row
				if len(cell) > 0:
					new_list.append(cell[0].text or "")	# Append the cell data to the new list
		return xmlData

import csv

class writeOutToCSVFile:
	"""writing out a CSV file
	"""
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

	def writeOutCsvBody(self, theOutList, outFileName):
		"""write out the CSV body
		
		:param theOutList: list that needs to be written out
		:param outFileName: string that has the pathfilename
		"""

	def doWriteOut(self, outFileName, theOutList):
		"""Calls the other function which do the write out of the CSV file
	
		:param outFileName: string which has the pathfilename
		:param theOutList: the list to write out
		"""
		outFilePtr = self.openCSVFile(outFileName)			# start at the same folder as the input file was located
#		self.writeOutputHeader(theOutList, outFilePtr)		# write out the header
		outFilePtr.writerows(theOutList)					# write out the BOM list to the output CSV file

	def sortMyList(self, inList):
		"""sorting a list
		
		:param inList: The list to sort
		:returns: the sorted list
		"""
		print 'Sorting lists'
		dirFileList = sorted(dirFileList1, key = lambda errs: errs[0])		# sort by Relative Path
		return dirFileList

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print "PyGtk 2.3.90 or later required"
   raise SystemExit

class FindACsvFile:
	def findCsvFile(self, startingPath):
		"""findCSVFile() - This is the dialog which locates the csv files
	
		:returns: path/name of the file that was selected
		"""
		csvFileString = "Select file"
		dialog = gtk.FileChooserDialog(csvFileString,
	                               None,
	                               gtk.FILE_CHOOSER_ACTION_OPEN,
	                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		if startingPath != '':
			dialog.set_current_folder(startingPath)
		filter = gtk.FileFilter()
		filter.set_name("CSV files")
		filter.add_pattern("*.csv")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFileName = dialog.get_filename()
			dialog.destroy()
			return retFileName
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
		dialog.destroy()

class FindAXmlFile:
	"""Find XML file with the file chooser dialog
	"""
	def findXmlFile(self, startingPath):
		"""FindAXmlFile() - This is the dialog which locates the xml files
		
		:param startingPath: the path to start the folder selector in
		:returns: path/name of the file that was selected
		"""
		csvFileString = "Select file"
		dialog = gtk.FileChooserDialog(csvFileString,
	                               None,
	                               gtk.FILE_CHOOSER_ACTION_OPEN,
	                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		if startingPath != '':
			dialog.set_current_folder(startingPath)
		filter = gtk.FileFilter()
		filter.set_name("XML files")
		filter.add_pattern("*.xml")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			retFileName = dialog.get_filename()
			dialog.destroy()
			return retFileName
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
			dialog.destroy()
			exit()
		dialog.destroy()

class CheckFreshness():
	"""Check to see if the file was saved today.
	Ignores midnight
	"""
	def isFresh(self, pathFileName):
		"""Check to see if a file is fresh (shares the same date as today)
		Uses global freshnessCheck
		
		:param pathFileName: Pathfilename to check
		:returns: True if the date matches today's date, false otherwise
		"""
		if not freshnessCheck:
			return True
		t = os.path.getmtime(pathFileName)
		fileTimeDateStamp = datetime.datetime.fromtimestamp(t)
		fileDateStamp = str(fileTimeDateStamp)
		fileDateStamp = fileDateStamp[0:fileDateStamp.find(' ')]
		currentDate = time.strftime("%Y-%m-%d")
		if fileDateStamp == currentDate:
			return True
		else:
			return False

def errorDialog(errorString):
	"""
	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return
			
			
