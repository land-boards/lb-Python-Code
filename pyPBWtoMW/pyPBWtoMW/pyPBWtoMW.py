'''pyPBWtoMW - Convert PBWorks wiki pages to MediaWiki wiki pages.
Handles simpler html tags which make for most of the data.

=====
INPUT
=====

Select input file via browser. 

======
OUTPUT
======

Output file is named the same as the input file with extension changed to .mw.
'''

import string

import pygtk
pygtk.require('2.0')

import gtk

# Check for new pygtk: this is new class in PyGtk 2.4
if gtk.pygtk_version < (2,3,90):
   print "PyGtk 2.3.90 or later required"
   raise SystemExit

class FindAFile:
	def findFile(self, startingPath):
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
		filter.set_name("All files")
		filter.add_pattern("*.*")
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


def processListItem(strToProcess):
	'''process the list items LI lines
	'''
	global indentLevelUL
	outStr = strToProcess
	outStart = ''
	if string.find(outStr,'<li>') != -1:
		outStr = string.replace(outStr, '<li>','')
		if unorderedListFlag == True:
			outStart = '*' * indentLevelUL
		elif unorderedListFlag == False:
			outStart = '#' * indentLevelOL
	if string.find(outStr,'</li>') != -1:
		outStr = string.replace(outStr,'</li>',"")
	outStr = outStart + ' ' + outStr
	return outStr

def processListTagUL(strToProcess):
	'''process the unordered list tags
	'''
	global unorderedListFlag
	global indentLevelUL
	outString = strToProcess
	if string.find(strToProcess, "<ul>") != -1:
		outString = string.replace(strToProcess, "<ul>", '')
		indentLevelUL += 1
	elif string.find(strToProcess, "</ul>") != -1:
		outString = string.replace(strToProcess, "</ul>", '')
		indentLevelUL -= 1
	unorderedListFlag = True
	return outString

def processListTagOL(strToProcess):
	'''process the ordered list tags
	'''
	global unorderedListFlag
	global indentLevelOL
	outString = strToProcess
	if string.find(strToProcess, "<ol>") != -1:
		outString = string.replace(strToProcess, "<ol>", '')
		indentLevelOL += 1
	elif string.find(strToProcess, "</ol>") != -1:
		outString = string.replace(strToProcess, "</ol>", '')
		indentLevelOL -= 1
	unorderedListFlag = False
	return outString

def processHeader(strToProcess):
	''' process the header lines
	'''
	inStr = strToProcess
	headerStart = string.find(inStr, '<h')
	headerLevel = inStr[headerStart+2]
	headerEnd = string.find(inStr,'</h')
	outStr = inStr[headerStart+4:headerEnd]
	outStartEnd = '=' * int(headerLevel)
	outStrFixed = outStartEnd + ' ' + outStr + ' ' + outStartEnd
	return outStrFixed

def processImageTag(strToProcess):
	'''Change this
	<img id="pbImage918288" src="/f/iTheremin-2.jpg" alt="" />
	into this
	[[File:iTheremin-2.jpg]]
	'''
	inStr = strToProcess
	outStr = ''
	imgStart = string.find(inStr, '<img')
	pathStart = string.find(inStr, '\"')
	pathEnd = string.find(inStr, '\"', pathStart + 1)
	print inStr[pathStart:pathEnd]
	if imgStart > 0:
		outStr = inStr[0:imgStart]
	return outStr

def processAHref(strToProcess):
	'''href string format is:
	<a href="/w/page/55092684/FTDI%20USB%20TTL" search_id="undefined">FTDI</a>
	'''
	print 'processingAHref line', strToProcess
	inStr = strToProcess
	outStr = ''
	ahrefStart = string.find(inStr, '<a href=')
	if ahrefStart > 0:
		outStr = inStr[0:ahrefStart]
	pathStart = string.find(inStr,'\"',ahrefStart+5)
	if pathStart == -1:
		print 'expected path to follow the a href line:', inStr
	pathEnd = string.find(inStr,'\"',pathStart+2)
	if pathEnd == -1:
		print 'expected path end', inStr
	outStr = '[['
	outStr += inStr[pathStart+1:pathEnd]
	outStr += '|'
	tagStart = string.find(inStr,">",pathEnd)
	tagEnd = string.find(inStr,"</a>",tagStart)
	outStr += inStr[tagStart+1:tagEnd]
	outStr += ']]'
	
	print 'ahref out', outStr
	return outStr

def processTableHeader(strToProcess):
	'''Line looks like:
	<table border="0" cellspacing="0" cellpadding="0" width="416">
	'''
	outStr = '{| class="wikitable"'
	return outStr
	
def processTableEnd(strToProcess):
	'''Line looks like:
	</table>
	'''
	outStr = '|}'
	return outStr
		
def processTableData(strToProcess):
	'''Line looks like:
	<td style="height: 20px; width: 93px;" width="93" height="20">Iforward</td>
	'''
	outStr = '|'
	textStr = strToProcess[string.find(strToProcess,'>')+1:string.rfind(strToProcess,'<')]
	outStr += textStr
	return outStr
	
def processTableRowEnd(strToProcess):
	'''Line looks like:
	</tr>
	'''
	outStr = ''
	return outStr

def processTableRowStart(strToProcess):
	'''Line looks like:
	<tr>
	'''
	outStr = '|-'
	return outStr

def reformatLine(strToFormat):
	'''deal specifically with lists and headers
	'''
	outLine = strToFormat
	keepDoingIt = True
	while keepDoingIt == True:
		keepDoingIt = False
		if string.find(outLine, "ul>") != -1:
			outLine = processListTagUL(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found ul'
		elif string.find(outLine, 'ol>') != -1:
			outLine = processListTagOL(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found ol'
		elif string.find(outLine, "li>") != -1:
			outLine = processListItem(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found li'
		elif string.find(outLine, "<h") != -1:
			outLine = processHeader(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found <h'
		elif string.find(outLine, '<img ') != -1:
			outLine = processImageTag(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found img'
		elif string.find(outLine, '<a href=') != -1:
			outLine = processAHref(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'got an href'
		elif string.find(outLine, '<table') != -1:
			outLine = processTableHeader(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found table start'
			processingTable = True
		elif string.find(outLine, '</table>') != -1:
			outLine = processTableEnd(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found end table'
			processingTable = False
		elif string.find(outLine, '<tr>') != -1:
			outLine = processTableRowStart(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found table row start'
		elif string.find(outLine, '</tr>') != -1:
			outLine = processTableRowEnd(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found table row end'
		elif string.find(outLine, '<td') != -1:
			outLine = processTableData(outLine)
			keepDoingIt = True
			if printParse == True:
				print 'found table row end'
		else:
			keepDoingIt = False
	return outLine

def removeJunk(strToFormat):
	''' remove stuff that can be easily removed
	'''
	if strToFormat == '<p>&nbsp;</p>':
#		print 'should print a blank line'
		return ''
	stringStart = string.find(strToFormat, '<p>')
	if stringStart != -1:
		if stringStart == 0:
			strToFormat = strToFormat[3:]
		else:
			startString = strToFormat[0:stringStart]
			endString = strToFormat[stringStart+3:]
			strToFormat = startString + endString
	stringStart = string.find(strToFormat, '</p>')
	if stringStart != -1:
		if stringStart == 0:
			strToFormat = strToFormat[4:]
		else:
			startString = strToFormat[0:stringStart]
			endString = strToFormat[stringStart+4:]
			strToFormat = startString + endString
	stringStart = string.find(strToFormat, '<br />')
	if stringStart != -1:
		if stringStart == 0:
			strToFormat = strToFormat[6:]
		else:
			startString = strToFormat[0:stringStart]
			endString = strToFormat[stringStart+6:]
			strToFormat = startString + endString
	keepUp = 1
	while keepUp == 1:
		keepUp = 0
		if string.find(strToFormat, '<span') != -1:
#			print 'found a span'
			startSpan = string.find(strToFormat, '<span')
			endSpan = string.find(strToFormat,'>',startSpan+1)
#			print 'startSpan', startSpan
#			print 'endSpan', endSpan
			if startSpan == 0:
				strToFormat = strToFormat[endSpan+1:]
			else:
				startOfString = strToFormat[0:startSpan]
				endOfString = strToFormat[endSpan+1:]
				strToFormat = startOfString + endOfString
			keepUp = 1
#			print 'with span removed', strToFormat
		if string.find(strToFormat, '</span>') != -1:
#			print 'found an end span'
			startSpan = string.find(strToFormat, '</span>')
			if startSpan == 0:
				strToFormat = strToFormat[startSpan+7:]
			else:
				startOfString = strToFormat[0:startSpan]
				endOfString = strToFormat[startSpan+7:]
				strToFormat = startOfString + endOfString
	
	return strToFormat

printParse = False

myFile = FindAFile()
inFilePathName = myFile.findFile('')

extensionColumn = string.rfind(inFilePathName, '.')

outFilePathName = inFilePathName[0:extensionColumn] + '.mw'

inPtr = open(inFilePathName, 'r')
outPtr = open(outFilePathName, 'w')

indentLevelUL = 0
indentLevelOL = 0
unorderedListFlag = True

for inLine in inPtr:
	inLine = inLine.strip('\n\r')
	outLine = ''
	outLine = removeJunk(inLine)
	outLine = reformatLine(outLine)
	outPtr.write(outLine + '\n')
