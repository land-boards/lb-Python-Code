"""
pyMWToHTML.py
Convert a <edia Wiki section to HTML
"""

# import string
# import sys
# from sys import version_info

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def countLevel(line):
	level = 0
	while line[level] == '=':
		level+=1
	# print("level",level)
	return level

def countStars(line):
	level = 0
	while line[level] == '*':
		level+=1
	# print("stars",level)
	return level

inList = readFileToListOfStrings('test.MW')
oldStarLevel = 0
for row in inList:
	headerLevel = 0
	if len(row) > 0:
		if '[' in row:
			row = row.replace('[',"<a href=\"")
			row = row +"</a>"
		if row[0] == '=':
			headerLevel = countLevel(row)
			print("<h",end='')
			print(headerLevel,end='')
			print(">",end='')
			print(row[headerLevel+1:len(row)-(2*headerLevel)+1],end='')
			print("</h",end='')
			print(headerLevel,end='')
			print(">")
		elif row[0] == '*':
			indentStarLevel = countStars(row)
			if indentStarLevel > oldStarLevel:
				print("<ul>")
				print("<li>",end='')
				print(row[indentStarLevel+1:],end='')
				print("</li>")
			elif indentStarLevel < oldStarLevel:
				print("</ul>")
				print("<li>",end='')
				print(row[indentStarLevel+1:],end='')
				print("</li>")
			else:
				print("<li>",end='')
				print(row[indentStarLevel+1:],end='')
				print("</li>")
			oldStarLevel = indentStarLevel
		else:
			print(row)
for todoends in range(oldStarLevel):
	print("</ul>")
	
