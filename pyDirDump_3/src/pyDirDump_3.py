"""Dump the contents of a directory (folder) and the subdirectories (folders) 
below that directory into a CSV file.

=====
USAGE
=====

- Browse to the folder you want to read.
- Result will be saved into c: backslash temp backslash dirList.csv

"""
import os
from win32com.shell import shell, shellcon
import csv

from tkinter import filedialog as fd
from tkinter import *
from tkinter import messagebox

def browseToFolder():
	"""
	:return: path/filename of the selected folder
	
	Opens a windows folder browser to allow user to navigate to the folder to read.

	"""
	root = Tk()
	root.directory = fd.askdirectory()
	return root.directory

path = browseToFolder()

dirString = ('dir /-c /n /s \"')
dirString += path
dirString += '\" > c:\\temp\\tempFile.txt'
if os.system(dirString) != 0:
	print('failed to open directory')
	exit()

readFile = open("c:\\temp\\tempFile.txt", 'r')
outFileName = 'c:\\temp\\fileList.csv'
writeFile = open(outFileName, "w")

lookingForVolName = 0
lookingForVolSer = 1
lookingForBlankLineFirst = 2
lookingForDirName = 3
lookingForBlankLineSecond = 4
lookingForDirFirst = 5
lookingForDirSecond = 6
lookingForLines = 7

filesReadCount = 0
numberOfDirs = 0
stateValue = lookingForVolName

for line in readFile:
	line = line.strip('\r\n')
	if stateValue == lookingForVolName:
		if line.find('Volume in drive') <= 0:
			print('expected a "Volume" as the first string on the first line')
			print(line)
			exit()
		elif len(line) < 24:
			print("String is too short to be a volume string. Expected > 24 characters, got %s" % len(line))
			print(" String is: %s" % dirLineBuffer)
		outLineBuffer = line[1:] + '\r'
		writeFile.write(outLineBuffer)
		stateValue = lookingForVolSer
	elif stateValue == lookingForVolSer:
		writeFile.write('Date,Time,Size,FileName,DirectoryName\n')
		if line.find('Volume Serial Number is ') <= 0:
			print('Expected to find Volume Serial Number is')
			print('instead got %s',line)
		stateValue = lookingForBlankLineFirst
	elif stateValue == lookingForBlankLineFirst:
		if len(line) > 0:
			print('Was looking for a blank line as the third line in the file')
			print('line is ',),
			print(len(line)),
			print(' long')
			exit()
		stateValue = lookingForDirName
	elif stateValue == lookingForDirName:
		if line[0] != ' ':
			print('Expected a space as the first character on the directory line')
			exit()
		elif line.find('Total Files Listed:') > 0:
			print('Read path: ', path)
			print('Num files: ', filesReadCount)
			print('Num dirs:  ', numberOfDirs)
			exit()
		elif line.find('Directory of ') <= 0:
			print('Expected string "Directory of" as the second character on the directory line - got %s' % line[1:14])
			exit()
		elif len(line) < 15:
			print('String is too short to be a volume string. Expected > 16 characters')
			exit()
		directoryName = line[14:]
		stateValue = lookingForBlankLineSecond
	elif stateValue == lookingForBlankLineSecond:
		if len(line) > 0:
			print('Was looking for a blank line after the directory name')
			exit()
		stateValue = lookingForDirFirst
	elif stateValue == lookingForDirFirst:
		if line.find('<DIR>') <= 0:
			dateString = line[0:10]
			timeString = line[12:20]
			sizeString = line[28:38]
			sizeString = sizeString.strip()
			fileNameString = line[39:]
			outLineBuffer = ""
			outLineBuffer = dateString
			outLineBuffer += ','
			outLineBuffer += timeString
			outLineBuffer += ','
			outLineBuffer += sizeString
			outLineBuffer += ','
			outLineBuffer += '\"'
			outLineBuffer += fileNameString
			outLineBuffer += '\"'
			outLineBuffer += ','
			outLineBuffer += '\"'
			outLineBuffer += directoryName
			outLineBuffer += '\"'
			#outLineBuffer += '\n'
			writeFile.write(outLineBuffer)
			filesReadCount += 1
			stateValue = lookingForLines
		else:
			stateValue = lookingForDirSecond
	elif stateValue == lookingForDirSecond:
		if line.find('<DIR>') <= 0:
			dateString = line[0:10]
			timeString = line[12:20]
			sizeString = line[28:38]
			sizeString = sizeString.strip()
			fileNameString = line[39:]
			outLineBuffer = ""
			outLineBuffer = dateString
			outLineBuffer += ','
			outLineBuffer += timeString
			outLineBuffer += ','
			outLineBuffer += sizeString
			outLineBuffer += ','
			outLineBuffer += '\"'
			outLineBuffer += fileNameString
			outLineBuffer += '\"'
			outLineBuffer += ','
			outLineBuffer += '\"'
			outLineBuffer += directoryName
			outLineBuffer += '\"'
			#outLineBuffer += '\n'
			writeFile.write(outLineBuffer)
			filesReadCount += 1
			stateValue = lookingForLines
		else:
			stateValue = lookingForLines
	elif stateValue == lookingForLines:
		if line[0] == ' ':
			stateValue = lookingForBlankLineFirst
		elif line.find('<DIR>') <= 0:
			dateString = line[0:10]
			timeString = line[12:20]
			sizeString = line[28:38]
			sizeString = sizeString.strip()
			fileNameString = line[39:]
			outLineBuffer = ""
			outLineBuffer = dateString
			outLineBuffer += ','
			outLineBuffer += timeString
			outLineBuffer += ','
			outLineBuffer += sizeString
			outLineBuffer += ','
			outLineBuffer += '\"'
			outLineBuffer += fileNameString
			outLineBuffer += '\"'
			outLineBuffer += ','
			outLineBuffer += '\"'
			outLineBuffer += directoryName
			outLineBuffer += '\"'
			outLineBuffer += '\n'
			writeFile.write(outLineBuffer)
			filesReadCount += 1
		elif line.find('<DIR>',24) > 0:
			numberOfDirs += 1
