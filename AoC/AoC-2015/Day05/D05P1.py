def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	return inList

def isNaughty(strToCheck):
	vowels = 'aeiou'
	gotDouble = False
	for charOffset in range(len(strToCheck)-1):
		if strToCheck[charOffset] == strToCheck[charOffset+1]:
			print(strToCheck[charOffset],strToCheck[charOffset+1])
			gotDouble = True
	if not gotDouble:
		print('no double')
		return True
	if 'ab' in strToCheck:
		print('had ab')
		return True
	elif 'cd' in strToCheck:
		print('had cd')
		return True
	elif 'pq' in strToCheck:
		print('had pq')
		return True
	elif 'xy' in strToCheck:
		print('had xy')
		return True
	vowelCount = 0
	for charCheck in strToCheck:
		if charCheck in vowels:
			vowelCount += 1
	if vowelCount < 3:
		print('<3 vowels')
		return True
	return False
		

inList = readFileToList()
# inList = ['ugknbfddgicrmopn','aaa','jchzalrnumimnmhp','haegwjzuvuyypxyu','dvszwmarrgswjxmb']
countOfNaughty = 0
countOfNice = 0
for line in inList:
	print("checking",line,end=' ')
	if isNaughty(line):
		print('naughty')
		countOfNaughty += 1
	else:
		print('nice')
		countOfNice += 1
print('Naughty =',countOfNaughty)
print('Nice =',countOfNice)
