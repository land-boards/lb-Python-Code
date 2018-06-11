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
		theBiometricsList = myCSVFileReadClass.findOpenReadCSV(defaultPath,'Select Biometrics CSV File')	# read in CSV into list
		if theBiometricsList == []:
			return False
		fileToWrite = myCSVFileReadClass.getLastPathFileName()[0:-4] + '_OUT.CSV'
		#print 'fileToWrite',fileToWrite
		try:
			outFile = open(fileToWrite, 'wb')
		except IOError:
			errorDialog('ERROR - Cannot open the output file.\nIs the file already open?\nClose the file and return.')
			try:
				outFile = open(fileToWrite, 'wb')
			except IOError:
				errorDialog('ERROR - Tried again,  - Is the file already open?')
				exit()
		
		myCSVFileWriteClass = WriteListtoCSV()
		myCSVFileWriteClass.setVerboseMode(True)	# turn on verbose mode until all is working 
		header = ['Date','Protein(g)','Fat(g)','Carbs(g)']

		servingsList = self.crunchServingsList(theServingsList)

		biometricsList = self.crunchBiosList(theBiometricsList)

#		theOutList = self.combineDataLists(theServingsList, theBiometricsList)
		
		myCSVFileWriteClass.writeOutList(fileToWrite, header, servingsList)
		
	def crunchServingsList(self, servingsList):
		"""
		:param outFilePtr: Points to the output file.
		:param servingsList: The servings list.
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
		dateColumn = int(servingsDictionary['Day'])
		proteinColumn = int(servingsDictionary['Protein (g)'])
		fatColumn = int(servingsDictionary['Fat (g)'])
		carbsColumn = int(servingsDictionary['Net Carbs (g)'])
		lastDay = servingsList[1][dateColumn]
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
			if row[dateColumn] != lastDay:	# Write out the previous list
				dayRow = []
				dayRow.append(lastDay)
				dayRow.append(str(totalProtein))
				dayRow.append(str(totalFat))
				dayRow.append(str(totalCarbs))
				shortServingsList.append(dayRow)
#				print 'dayRow',dayRow
				totalProtein = 0.0
				totalFat = 0.0
				totalCarbs = 0.0
				lastDay = row[dateColumn]
			if row[proteinColumn] != '':
				totalProtein += float(row[proteinColumn])
			if row[fatColumn] != '':
				totalFat += float(row[fatColumn])
			if row[carbsColumn] != '':
				totalCarbs += float(row[carbsColumn])
		dayRow.append(lastDay)
		dayRow.append(str(totalProtein))
		dayRow.append(str(totalFat))
		dayRow.append(str(totalCarbs))
		shortServingsList.append(dayRow)
#		print 'shortServingsList',shortServingsList
		return shortServingsList
		
	def crunchBiosList(self, biometricsList):
		"""
		:param outFilePtr: Points to the output file.
		:param crunchBiosList: The biometrics list.
		
		12/14/2017,Weight (Nokia),lbs,183.731
		12/14/2017,Body Fat (Nokia),%,19.751

		"""
		biosHeader = ['Day','Metric','Unit','Amount']
		biosDictionary = {}
		i = 0
		for element in biosHeader:
			biosDictionary[element] = i
			i = i + 1
		print 'dictionary is: ', biosDictionary
		shortBiosList = []
		dateColumn = int(biosDictionary['Day'])
		metricColumn = int(biosDictionary['Metric'])
		unitColumn = int(biosDictionary['Unit'])
		amountColumn = int(biosDictionary['Amount'])
		offsetRow = 1
		for row in biometricsList[1:]:
			if row[metricColumn] == 'Body Fat (Nokia)':
				lastDate = row[dateColumn]
				lastWeight = float(row[amountColumn])
				offsetRow += 1
				break
		dayRow = []
		for row in biometricsList[offsetRow:]:
			if row[dateColumn] != lastDate:	# Write out the previous list
				dayRow = []
				dayRow.append(lastDate)
				dayRow.append(str(lastWeight))
				shortBiosList.append(dayRow)
				lastWeight = 9999.99
			if row[metricColumn] == 'Body Fat (Nokia)':
				if float(row[amountColumn]) < lastWeight:
					lastWeight = row[amountColumn]
		dayRow.append(lastDate)
		dayRow.append(str(lastWeight))
		shortBiosList.append(dayRow)
		print shortBiosList
		return shortBiosList
			
		
	def combineDataLists(self, servingsList, biometricsList):
		"""
		:param outFilePtr: Points to the output file.
		:param servingsList: The servings list.
		:param servingsList: The biometrics list.

		"""
		
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
