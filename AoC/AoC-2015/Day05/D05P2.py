# Day 5 Part 2

def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	return inList

def isNaughty(strToCheck):
	gotDouble = False
	for charOffset in range(len(strToCheck)-2):
		if strToCheck[charOffset] == strToCheck[charOffset+2]:
			print("1st check repeated with space :",strToCheck[charOffset:charOffset+3])
			gotDouble = True
			break
	if not gotDouble:
		print('no double')
		return True
	got2ndDouble = False
	for charOffset in range(len(strToCheck)-2):
		print("Checking",strToCheck[charOffset:charOffset+2],end=' ')
		for substrOffset in range(charOffset+2,len(strToCheck)-1):
			print("against",strToCheck[substrOffset:substrOffset+2])
			if strToCheck[charOffset:charOffset+2] == strToCheck[substrOffset:substrOffset+2]:
				print("Got 2nd double",strToCheck[substrOffset:substrOffset+2])
				got2ndDouble = True
				return False
	if got2ndDouble == True:
		return False
	return True
		

inList = readFileToList()
#inList = ['qjhvhtzxzqqjkmpb','xxyxx','uurcxstgmygtbstg','ieodomkazucvgmuy']
countOfNaughty = 0
countOfNice = 0
for line in inList:
	print("\nchecking string :",line)
	if isNaughty(line):
		print('naughty')
		countOfNaughty += 1
	else:
		print('nice')
		countOfNice += 1
print('Naughty =',countOfNaughty)
print('Nice =',countOfNice)
