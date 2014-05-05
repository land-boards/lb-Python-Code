###########################################################################################
# Some common Python Patterns

###########################################################################################
# Path/filename extraction
import string

# Extract Path from fullPathFilename
def	extractPathFromPathfilename(fullPathFilename):
	return(fullPathFilename[0:fullPathFilename.rfind('\\')+1])

# Extract fileName without extension from pathfullPathName
def extractFilenameFromPathfilename(fullPathFilename):
	return(fullPathFilename[fullPathFilename.rfind('\\')+1:-4])

# Extract fileName from pathfullPathName
def extractFilenameNoextFromPathfilename(fullPathFilename):
	return(fullPathFilename[fullPathFilename.rfind('\\')+1:])

### Test Code
testFullpathFilename = 'c:\\mypath\doug.csv'

print extractPathFromPathfilename(testFullpathFilename)
print extractFilenameFromPathfilename(testFullpathFilename)
print extractFilenameNoextFromPathfilename(testFullpathFilename)

###########################################################################################
# reading in an XML file

# Use the ElementTree module but alias it as "Xml"
import xml.etree.ElementTree as Xml

# XMLtoList class reads the XML file into a list
class XMLtoList:
	# returns list which contains the XML spreadsheet data
	def readSpreadsheetXML2List(self, inFileN):
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

		
###########################################################################################
# writing out a CSV file

import csv

class writeOutToCSVFile:

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

	def writeOutCsvBody(self, theOutList, outFileName):
		outFilePtr = self.openCSVFile(outFileName)			# start at the same folder as the input file was located
#		self.writeOutputHeader(theOutList, outFilePtr)		# write out the header
		outFilePtr.writerows(theOutList)					# write out the BOM list to the output CSV file

###########################################################################################
# sorting a list

	print 'Sorting lists'
	dirFileList1 = sorted(dirFileList1, key = lambda errs: errs[0])		# sort by Relative Path

###########################################################################################
# findCSVFile() - This is the dialog which locates the csv files
# Function returns the path/name of the file that was selected

class FindACsvFile:
	def findCsvFile(self, startingPath):
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

###########################################################################################
# FindAXmlFile() - This is the dialog which locates the xml files
# Function returns the path/name of the file that was selected

class FindAXmlFile:
	def findXmlFile(self, startingPath):
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

	
