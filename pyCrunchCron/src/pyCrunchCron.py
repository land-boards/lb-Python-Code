"""
=================
pyCrunchCron.py
=================

Crunch a set of Cronometer files.

==========
Background
==========

Cronometer is a diet tracker.
Cronometer dumps out data as a .csv (EXCEL) file.
This program takes the output file from Cronometer and creates a reduced data set.

=====
Usage
=====

This program prompts for macros and biometrics files.
The output file is created in the same path with as CronCrunch-YY-MM-DD.csv

===
API
===

"""

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
	 print "PyGtk 2.3.90 or later required"
	 raise SystemExit

import csv
import string
import os
import sys

sys.path.append('C:\\Users\\Doug\\Documents\\GitHub\\lb-Python-Code\\dgCommonModules')
sys.path.append('C:\\HWTeam\\Utilities\\dgCommonModules')

from dgProgDefaults import *
from dgReadCSVtoList import *
from dgWriteListtoCSV import *
defaultPath = '.'

from sys import argv

def errorDialog(errorString):
	"""
	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return
	
class ControlClass:
	def theExecutive(self):
		"""
		:global lastPathFileName: The path and file name that was found by the browser.

		The code that calls the other code.
		This code uses the defaults library to handle the default path.
		This code uses the read CSV library to read in the CSV file.
		"""
		global defaultPath
		
		defaultParmsClass = HandleDefault()
		defaultParmsClass.initDefaults()
		defaultPath = defaultParmsClass.getKeyVal('DEFAULT_PATH')
		#print 'defaultPath',defaultPath

		myCSVFileReadClass = ReadCSVtoList()	# instantiate the class
		myCSVFileReadClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		theServingsList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select Servings CSV File')	# read in CSV into list
		if theServingsList == []:
			return False
		servingsList = self.crunchServingsList(theServingsList)

		biometricsList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select Biometrics CSV File')	# read in CSV into list
		if biometricsList == []:
			return False
		weightFileToWrite = myCSVFileReadClass.getLastPath() + 'pyCronCrunch_Weight.CSV'
		#print 'weightFileToWrite',weightFileToWrite
		try:
			outFile = open(weightFileToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(weightFileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		myCSVFileWriteClass = WriteListtoCSV()
		myCSVFileWriteClass.setVerboseMode(True)	# turn on verbose mode until all is working 

		weightBiometricList = self.crunchWeightList(biometricsList)
		header = ['Date','Protein(g)','Fat(g)','Carbs(g)','Calories','Weight(lbs)','Weight Change(lbs)']
		theOutList = self.combineTwoLists(servingsList, weightBiometricList)
		myCSVFileWriteClass.writeOutList(weightFileToWrite, header, theOutList)

		bloodGlucoseFileToWrite = myCSVFileReadClass.getLastPath() + 'pyCronCrunch_Glucose.CSV'
		try:
			outFile = open(bloodGlucoseFileToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(bloodGlucoseFileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		myCSVFileWriteClass = WriteListtoCSV()
		myCSVFileWriteClass.setVerboseMode(True)	# turn on verbose mode until all is working 

		weightBiometricList = self.crunchGlucoseList(biometricsList)
		header = ['Date','Protein(g)','Fat(g)','Carbs(g)','Calories','Blood Glucose(mg/dl)']
		theOutList = self.combineTwoLists(servingsList, weightBiometricList)
		myCSVFileWriteClass.writeOutList(bloodGlucoseFileToWrite, header, theOutList)

		
	def crunchServingsList(self, servingsList):
		"""
		:param servingsList: The servings list.
		
		:returns: list of ['Date','Protein','Fat','Carbs','Calories']
		
		Take the foods and sum up the Protein, Fat and Carbs for each food item.
		"""
		servingsHeader = ['Day','Food Name','Amount','Energy (kcal)','Alcohol (g)',\
		'Caffeine (mg)','Water (g)','B1 (Thiamine) (mg)','B2 (Riboflavin) (mg)',\
		'B3 (Niacin) (mg)','B5 (Pantothenic Acid) (mg)','B6 (Pyridoxine) (mg)',\
		'B12 (Cobalamin) (ug)','Folate (ug)','Vitamin A (IU)','Vitamin C (mg)',\
		'Vitamin D (IU)','Vitamin E (mg)','Vitamin K (ug)','Calcium (mg)','Copper (mg)',\
		'Iron (mg)','Magnesium (mg)', 'Manganese (mg)','Phosphorus (mg)','Potassium (mg)',\
		'Selenium (ug)','Sodium (mg)','Zinc (mg)','Carbs (g)','Fiber (g)','Starch (g)',\
		'Sugars (g)','Net Carbs (g)','Fat (g)','Cholesterol (mg)','Monounsaturated (g)',\
		'Omega-3 (g)','Omega-6 (g)','Polyunsaturated (g)','Saturated (g)','Trans-Fats (g)',\
		'Cystine (g)','Histidine (g)','Isoleucine (g)','Leucine (g)','Lysine (g)','Methionine (g)',\
		'Phenylalanine (g)','Protein (g)','Threonine (g)','Tryptophan (g)','Tyrosine (g)','Valine (g)']
		servingsDictionary = {}
		i = 0
		for element in servingsHeader:
			servingsDictionary[element] = i
			i = i + 1
		#print 'dictionary is: ', servingsDictionary
		shortServingsList = []
		dateColumnOffset = int(servingsDictionary['Day'])
		proteinColumn = int(servingsDictionary['Protein (g)'])
		fatColumn = int(servingsDictionary['Fat (g)'])
		carbsColumn = int(servingsDictionary['Net Carbs (g)'])
		lastDay = servingsList[1][dateColumnOffset]
		if servingsList[1][proteinColumn] != '':
			lastProtein = float(servingsList[1][proteinColumn])
		else:
			lastProtein = 0.0
		if servingsList[1][fatColumn] != '':
			lastFat = float(servingsList[1][fatColumn])
		else:
			lastFat = 0.0
		if servingsList[1][carbsColumn] != '':
			lastCarbs = float(servingsList[1][carbsColumn])
		else:
			lastCarbs = 0.0
		totalProtein = 0.0
		totalFat = 0.0
		totalCarbs = 0.0
		dayRow = []
		for row in servingsList[2:]:
			if row[dateColumnOffset] != lastDay:	# Write out the previous list
				dayRow = []
				dayRow.append(lastDay)
				dayRow.append(str(totalProtein))
				dayRow.append(str(totalFat))
				dayRow.append(str(totalCarbs))
				totalCals = 4.0 * totalFat + 9.0 * totalProtein + 4.0 * totalCarbs
				dayRow.append(str(totalCals))
				shortServingsList.append(dayRow)
#				print 'dayRow',dayRow
				totalProtein = 0.0
				totalFat = 0.0
				totalCarbs = 0.0
				lastDay = row[dateColumnOffset]
			if row[proteinColumn] != '':
				totalProtein += float(row[proteinColumn])
			if row[fatColumn] != '':
				totalFat += float(row[fatColumn])
			if row[carbsColumn] != '':
				totalCarbs += float(row[carbsColumn])
		dayRow = []
		dayRow.append(lastDay)
		dayRow.append(str(totalProtein))
		dayRow.append(str(totalFat))
		dayRow.append(str(totalCarbs))
		shortServingsList.append(dayRow)
#		print 'shortServingsList',shortServingsList
		return shortServingsList
		
	def crunchWeightList(self, weightBiometricList):
		"""
		:param weightBiometricList: The biometrics list.
		:returns: ['Date','Weight(lbs)']
		
		12/14/2017,Weight (Nokia),lbs,183.731
		12/14/2017,Body Fat (Nokia),%,19.751
		1/4/2018,Blood Glucose,mg/dL,99
		5/13/2018,Ketones (Breath),ppm,4.1

		"""
		# Put the header into a dictionary to map the column numbers
		biosHeader = ['Day','Metric','Unit','Amount']
		# Mapping the header to column numbers allows access by header text
		biosDictionary = {}
		i = 0
		for element in biosHeader:
			biosDictionary[element] = i
			i = i + 1
		# print 'dictionary is: ', biosDictionary
		shortBiosList = []
		dateColumnOffset = int(biosDictionary['Day'])
		metricColumnOffset = int(biosDictionary['Metric'])
		unitColumnOffset = int(biosDictionary['Unit'])
		amountColumnOffset = int(biosDictionary['Amount'])
		lastWeight = 999.9
		reducedRows = []
		# Shorten the table to just weights
		for row in weightBiometricList[1:]:		# start after the header
			if row[metricColumnOffset] == 'Weight (Nokia)':
				reducedRows.append(row)
		lastDate = reducedRows[0][dateColumnOffset]				# The first date
		lastWeight = float(reducedRows[0][amountColumnOffset])	# The first weight
		dayRow = []
		for row in reducedRows[1:]:
			if row[dateColumnOffset] == lastDate:
				if float(row[amountColumnOffset]) < lastWeight:
					lastWeight = float(row[amountColumnOffset])
			if row[dateColumnOffset] != lastDate:	# Write out the previous list
				dayRow = []
				dayRow.append(lastDate)
				dayRow.append(str(lastWeight))
				shortBiosList.append(dayRow)
				#print 'date',lastDate,'weight',lastWeight
				# Save the current values to use next time
				lastDate = row[dateColumnOffset]
				lastWeight = float(row[amountColumnOffset])
#		print 'shortBiosList ', shortBiosList
		newShortBioList = []
		shortLine = shortBiosList[0]
		shortLine.append('0.0')
		newShortBioList.append(shortLine)
		lastWeight = float(shortBiosList[0][1])
		print 'lastWeight',lastWeight
		for row in shortBiosList[1:]:		 # assembly the list with deltas column
			shortLine = row
			shortLine.append(float(row[1])-lastWeight)
			lastWeight = float(row[1])
			newShortBioList.append(shortLine)
		return newShortBioList
			
	def crunchGlucoseList(self, glucoseList):
		"""
		:param weightBiometricList: The biometrics list.
		:returns: ['Date','Protein(g)','Fat(g)','Carbs(g)','Weight(lbs)']
		
		12/14/2017,Weight (Nokia),lbs,183.731
		12/14/2017,Body Fat (Nokia),%,19.751
		1/4/2018,Blood Glucose,mg/dL,99
		5/13/2018,Ketones (Breath),ppm,4.1

		"""
		# Put the header into a dictionary to map the column numbers
		biosHeader = ['Day','Metric','Unit','Amount']
		# Mapping the header to column numbers allows access by header text
		biosDictionary = {}
		i = 0
		for element in biosHeader:
			biosDictionary[element] = i
			i = i + 1
		# print 'dictionary is: ', biosDictionary
		shortGlucoseList = []
		dateColumnOffset = int(biosDictionary['Day'])
		metricColumnOffset = int(biosDictionary['Metric'])
		unitColumnOffset = int(biosDictionary['Unit'])
		amountColumnOffset = int(biosDictionary['Amount'])
		offsetRow = 1
		for row in glucoseList[1:]:
			if row[metricColumnOffset] == 'Blood Glucose':
				lastDate = row[dateColumnOffset]
				lastGlucose = float(row[amountColumnOffset])
				offsetRow += 1
				break
		dayRow = []
		for row in glucoseList[offsetRow:]:
			if row[dateColumnOffset] != lastDate:	# Write out the previous list
				dayRow = []
				dayRow.append(lastDate)
				dayRow.append(str(lastGlucose))
				if row[metricColumnOffset] == 'Blood Glucose':
					shortGlucoseList.append(dayRow)
					lastGlucose = 0.0
					if float(row[amountColumnOffset]) > lastGlucose:
						lastGlucose = row[amountColumnOffset]
				lastDate = row[dateColumnOffset]
		if row[metricColumnOffset] == 'Blood Glucose':
			dayRow.append(lastDate)
			dayRow.append(str(lastGlucose))
			shortGlucoseList.append(dayRow)
		return shortGlucoseList
			
	def combineTwoLists(self, list1, list2):
		"""
		:param list1: The first list.
		:param list2: The second list.
		:returns: combined list
		
		Combines two lists.
		Lists have date in the first column.
		First list comes first. Second list comes second.
		"""
		combinedList = []
		for rowList1 in list1:
			for rowList2 in list2:
				if rowList1[0] == rowList2[0]:
					combinedList.append(rowList1 + rowList2[1:])
					break
		return combinedList
		
class UIManager:
	"""The UI manager
	"""
	interface = """
	<ui>
		<menubar name="MenuBar">
			<menu action="File">
				<menuitem action="Open"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="Help">
				<menuitem action="About"/>
			</menu>
		</menubar>
	</ui>
	"""

	def __init__(self):
		"""Initialize the class
		"""
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
		window.set_title('pyCrunchCron - Kicad Parts List creation program')

		# Create an ActionGroup
		actiongroup =	gtk.ActionGroup("pyCrunchCron")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
									("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
									("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
									("File", None, "_File"),
									("Help", None, "_Help"),
									("About", None, "_About", None, "About pyCrunchCron", self.about_pyCrunchCron),
									])
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		"""Open the interface by calling the control class
		"""
		myControl = ControlClass()
		myControl.theExecutive()

		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("Conversion Complete")
		message.run()		# Display the dialog box and hang around waiting for the "OK" button
		message.destroy()	# Takes down the dialog box
		return

	def about_pyCrunchCron(self, b):
		"""The about dialog
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyCrunchCron\n(c) 2014 - Doug Gilliland\nAAC - All rights reserved\npyCrunchCron Create a mediawiki table frm a CV file")
		message.run()
		message.destroy()
		return

	def quit_application(self, widget):
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
