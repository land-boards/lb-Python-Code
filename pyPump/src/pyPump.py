"""
Reads in Minimed Insulin Pump CSV History file(s).

=====
Usage
=====

Program is run by either typing python pyPump.py or double clicking pyPump.py.

Select the Original reports then the Data Export (CSV).

======
Output
======


====
Code
====

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
import string

headerRow = 999

def errorDialog(errorString):
	"""
	:param errorString: the string to print

	Prints an error message as a dialog box
	"""
	message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	message.set_markup(errorString)
	message.run()		# Display the dialog box and hang around waiting for the "OK" button
	message.destroy()	# Takes down the dialog box
	return

class processPump:
	"""Class to process the Pump data.
	"""
	def selectPumpDataFile(self):
		"""
		:returns: path/name of the file that was selected. Empty string if none selected.
		
		This is the dialog which locates the Mouser files
		"""
		dialog = gtk.FileChooserDialog("Select csv file",
	                               None,
	                               gtk.FILE_CHOOSER_ACTION_OPEN,
	                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
	                               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

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
			dialog.destroy()
			return ''
	
	def readPumpData(self, partsFile):
		'''
		:param partsFile: location of the path/file name
		:returns: file contents as a list
		
		Read the parts file into a list for easier processing.
		'''
		partsFilePtr = open(partsFile,'rb')
		csvreader = csv.reader(partsFilePtr, delimiter=',', quotechar='|')
		pumpList = []
		for row in csvreader:
			pumpList.append(row)
		partsFilePtr.close()
		return pumpList

	def goThruInsulinData(self,newPumpList,pumpFileName):
		"""
		:param newPumpList: location of the path/file name
		:param pumpFileName: location of the path/file name
		:returns: True when completed
		
		Process the parts list.
		"""
		deliveredInsulinList = []
		for row in newPumpList:
			if len(row) > 33 and row[33] == 'ResultDailyTotal':
				print 'insulin',row[1],row[32]
				deliveredInsulinRow = []
				deliveredInsulinRow.append(row[1])
				deliveredInsulinRow.append(row[32])
				deliveredInsulinList.append(deliveredInsulinRow)
		outPumpList = pumpFileName[0:-4]
		outPumpList += '_Insulin.csv'
		outCSVFile = open(outPumpList, 'wb')
		outwriter = csv.writer(outCSVFile, delimiter=',')
		outwriter.writerows(deliveredInsulinList)
		return True		

	def goThruGlucoseData(self,newPumpList,pumpFileName):
		"""
		:param newPumpList: location of the path/file name
		:param pumpFileName: location of the path/file name
		:returns: True when completed
		
		Process the parts list.
		"""
		bloodGlucoseList = []
		lastDate = ''
		currentDate = ''
		totalGlucose = 0.0
		totalSamples = 0
		for row in newPumpList:
			if len(row) > 33 and (row[33] == 'BGCapturedOnPump' or row[33] == 'BGLifescan'):
				currentDate = row[1]
				# print 'currentDate',currentDate,'lastDate',lastDate
				if lastDate == '':
					totalGlucose += float(row[5])
					totalSamples = 1
					lastDate = currentDate
				elif lastDate == currentDate:
					totalGlucose += float(row[5])
					totalSamples += 1
				elif lastDate != currentDate:
					bloodGlucoseRow = []
					bloodGlucoseRow.append(lastDate)
					avgGlucose = 0.0
					avgGlucose = totalGlucose/(float(totalSamples))
					bloodGlucoseRow.append(avgGlucose)
					bloodGlucoseList.append(bloodGlucoseRow)
					#print 'BG',lastDate,avgGlucose
					totalGlucose = float(row[5])
					lastDate = currentDate
					totalSamples = 1
		bloodGlucoseRow.append(lastDate)
		avgGlucose = totalGlucose/(float(totalSamples))
		bloodGlucoseRow.append(avgGlucose)
		bloodGlucoseList.append(bloodGlucoseRow)
		outPumpList = pumpFileName[0:-4]
		outPumpList += '_BloodGlucose.csv'
		outCSVFile = open(outPumpList, 'wb')
		outwriter = csv.writer(outCSVFile, delimiter=',')
		outwriter.writerows(bloodGlucoseList)
		return True		
		
	def goThruCarbsData(self,newPumpList,pumpFileName):
		"""
		:param newPumpList: location of the path/file name
		:param pumpFileName: location of the path/file name
		:returns: True when completed
		
		Process the parts list.
		"""
		carbsList = []
		lastDate = ''
		currentDate = ''
		totalCarbs = 0.0
		totalSamples = 0
		for row in newPumpList:
			if len(row) > 33 and row[33] == 'BolusWizardBolusEstimate':
				currentDate = row[1]
				# print 'currentDate',currentDate,'lastDate',lastDate
				if lastDate == '':
					totalCarbs += float(row[23])
					totalSamples = 1
					lastDate = currentDate
				elif lastDate == currentDate:
					totalCarbs += float(row[23])
					totalSamples += 1
				elif lastDate != currentDate:
					carbsRow = []
					carbsRow.append(lastDate)
					carbsRow.append(totalCarbs)
					carbsList.append(carbsRow)
					print 'carbs',lastDate,totalCarbs
					totalCarbs = float(row[23])
					lastDate = currentDate
					totalSamples = 1
		carbsRow = []
		carbsRow.append(lastDate)
		carbsRow.append(totalCarbs)
		carbsList.append(carbsRow)
		outPumpList = pumpFileName[0:-4]
		outPumpList += '_Carbs.csv'
		outCSVFile = open(outPumpList, 'wb')
		outwriter = csv.writer(outCSVFile, delimiter=',')
		outwriter.writerows(carbsList)
		return True		
		
	def checkPumpFileHeader(self,entirePumpList):
		"""
		Medtronic Diabetes CareLink Personal Data Export File (v1.0.1) 
		PATIENT INFO
		Name,Douglas Gilliland
		Report Range,8/13/16,to,8/13/16
		DEVICE INFO
		Meter:,Linked Meter,#A6B7DB,,
		Pump:,Paradigm Revel - 723,#965788,VER 3.0B1.1,
		Data Exported on,8/13/16 10:05 AM
		DEVICE DATA (99 records)
		Data Range,8/13/16 00:00:00,to,8/13/16 09:50:55
		Index,Date,Time,Timestamp,New Device Time,BG Reading (mg/dL),Linked BG Meter ID,Temp Basal Amount (U/h),Temp Basal Type,Temp Basal Duration (hh:mm:ss),Bolus Type,Bolus Volume Selected (U),Bolus Volume Delivered (U),Bolus Duration (hh:mm:ss),Prime Type,Prime Volume Delivered (U),Suspend,Rewind,BWZ Estimate (U),BWZ Target High BG (mg/dL),BWZ Target Low BG (mg/dL),BWZ Carb Ratio (grams),BWZ Insulin Sensitivity (mg/dL),BWZ Carb Input (grams),BWZ BG Input (mg/dL),BWZ Correction Estimate (U),BWZ Food Estimate (U),BWZ Active Insulin (U),Alarm,Sensor Calibration BG (mg/dL),Sensor Glucose (mg/dL),ISIG Value,Daily Insulin Total (U),Raw-Type,Raw-Values,Raw-ID,Raw-Upload ID,Raw-Seq Num,Raw-Device Type

		"""
		global headerRow
		rowIndex = 0
		for row in entirePumpList:		
			if row[0] <> 'Index':
				rowIndex += 1
			else:
				headerRow = rowIndex
		if headerRow == 999:
			errorDialog('Could not find the header row.\nFirst element in the row must be Index')
			return False
		expectedHeader = ['Index','Date','Time','Timestamp','New Device Time','BG Reading (mg/dL)','Linked BG Meter ID','Temp Basal Amount (U/h)','Temp Basal Type','Temp Basal Duration (hh:mm:ss)','Bolus Type','Bolus Volume Selected (U)','Bolus Volume Delivered (U)','Bolus Duration (hh:mm:ss)','Prime Type','Prime Volume Delivered (U)','Suspend','Rewind','BWZ Estimate (U)','BWZ Target High BG (mg/dL)','BWZ Target Low BG (mg/dL)','BWZ Carb Ratio (grams)','BWZ Insulin Sensitivity (mg/dL)','BWZ Carb Input (grams)','BWZ BG Input (mg/dL)','BWZ Correction Estimate (U)','BWZ Food Estimate (U)','BWZ Active Insulin (U)','Alarm','Sensor Calibration BG (mg/dL)','Sensor Glucose (mg/dL)','ISIG Value','Daily Insulin Total (U)','Raw-Type','Raw-Values','Raw-ID','Raw-Upload ID','Raw-Seq Num','Raw-Device Type']
		if entirePumpList[headerRow] != expectedHeader:
			print 'Column header mismatched, expected'
			print expectedHeader
			print 'got header'
			print entirePumpList[111]
			offset = 0
			for cell in entirePumpList[11]:
				if cell != expectedHeader[offset]:
					print 'expected',expectedHeader[offset],'got',cell
				offset += 1
			return False
		print 'pump header matched'
		return True

	def doPumpProcessing(self):
		'''
		:returns: True when completed
		
		The executive which calls all of the other functions.
		'''
		global headerRow
		pumpFileName = self.selectPumpDataFile()
		if pumpFileName == '':
			errorDialog("Failed to open file")
			return False
		newPumpList = self.readPumpData(pumpFileName)
		if not self.checkPumpFileHeader(newPumpList):
			return False
		self.goThruInsulinData(newPumpList[headerRow+1:],pumpFileName)
		self.goThruGlucoseData(newPumpList[headerRow+1:],pumpFileName)
		self.goThruCarbsData(newPumpList[headerRow+1:],pumpFileName)
		return True
	
class UIManager:
	""" The UI
	"""
	interface = """
	<ui>
		<menubar name="MenuBar">
			<menu action="File">
				<menuitem action="Open"/>
				<menuitem action="Quit"/>
			</menu>
			<menu action="Options">
				<menuitem action="BackAnn"/>
				<menuitem action="Analyze"/>
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
		actiongroup =  gtk.ActionGroup("pyPump")
		self.actiongroup = actiongroup

		# Create actions
		self.actiongroup.add_actions([
			("Open", gtk.STOCK_OPEN, "_Open", None, "Open an Existing Document", self.openIF),
			("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the Application", self.quit_application),
			("File", None, "_File"),
			("Options", None, "_Options"),
			("Help", None, "_Help"),
			("About", None, "_About", None, "About pyPump", self.about_pymouserparts),
			])
		self.actiongroup.add_radio_actions([
			("BackAnn", gtk.STOCK_PREFERENCES, "_Back Annotate", '<Control>B', "Back annotate schematic from cmp file", 0),
			("Analyze", gtk.STOCK_PREFERENCES, "_Analyze", '<Control>A', "Analyze impact of backannotation", 1),
			], 2, self.setSelProcess)
		uimanager.insert_action_group(self.actiongroup, 0)
		uimanager.add_ui_from_string(self.interface)
		
		menubar = uimanager.get_widget("/MenuBar")
		vbox.pack_start(menubar, False)
		
		window.connect("destroy", lambda w: gtk.main_quit())
		
		window.add(vbox)
		window.show_all()

	def openIF(self, b):
		""" Read the file and process it
		"""
		partsClass = processPump()
		if partsClass.doPumpProcessing() != False:
			message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
			message.set_markup("Function Completed")
			message.run()
			message.destroy()
		return

	def about_pymouserparts(self, b):
		"""The about message
		"""
		message = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		message.set_markup("About pyPump\nAuthor: Doug Gilliland\n(c) 2014 - All rights reserved\nProgram takes Mouser records and creates one big PL")
		message.run()
		message.destroy()
		
	def setSelProcess(self, action, current):
		# global backAnnotate
		# text = current.get_name()
		# if (text == "BackAnn"):
			# backAnnotate = True
			# print 'Back annotate flag set'
		# elif (text == "Analyze"):
			# backAnnotate = False
			# print 'Analyze flag set'
		return

	def quit_application(self, widget):
		"""
		quit
		"""
		gtk.main_quit()

if __name__ == '__main__':
	ba = UIManager()
	gtk.main()
