# D04P1

def readFileOfStringsToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inLine = inLine.replace(' ',':')
			inList.append(inLine.split(':'))
	return inList

def isInRange(lower,upper,val):
	# Returns True if val is in the range from lower to upper
	# Return False otherwise
	return lower <= val <= upper

def isValidLength(expectedLength,strToCheck):
	# returns True if the strToCheck length is expectedLength
	# Return False otherwise
	return len(strToCheck) == expectedLength

DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

expectedFields = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
requiredFields = ['byr','iyr','eyr','hgt','hcl','ecl','pid']

def getFieldValue(key,record):
	for fieldOffset in range(len(record)):
		if record[fieldOffset] == key:
			return record[fieldOffset+1]
	debugPrint('key '+key+'')
	debugPrint('record '+record)
	assert False,'unexpected field'

def checkBYR(key,record):
	value = getFieldValue(key,record)
	debugPrint('byr '+value)
	year = int(value)
	return isInRange(1920,2002,year)

def checkIYR(key,record):
	value = getFieldValue(key,record)
	debugPrint('iyr '+value)
	year = int(value)
	return isInRange(2010,2020,year)

def checkEYR(key,record):
	value = getFieldValue(key,record)
	debugPrint('eyr '+value)
	year = int(value)
	return isInRange(2020,2030,year)

def checkHGT(key,record):
	value = getFieldValue(key,record)
	debugPrint('hgt '+value)
	if 'cm' in value:
		if not isValidLength(5,value):
			return False
		hgt = value[0:3]
		hgtNum = int(hgt)
		if isInRange(150,193,hgtNum):
			return True
		else:
			return False
	elif 'in' in value:
		if not isValidLength(4,value):
			return False
		hgt = value[0:2]
		hgtNum = int(hgt)
		if isInRange(59,76,hgtNum):
			return True
		else:
			return False
	else:
		return False
	assert False,"no clue how I got here"

def check_0to9_AtoF(charVal):
	debugPrint('check_0to9_AtoF '+charVal)
	if isInRange('a','f',charVal):
		return True
	if isInRange('0','9',charVal):
		return True
	else:
		print('failed check_0to9_AtoF')
		return False
		
def checkHCL(key,record):
	value = getFieldValue(key,record)
	debugPrint('hcl '+value)
	if value[0] != '#':
		return False
	if not isValidLength(7,value):
		return False
	for charVal in value[1:]:
		if not check_0to9_AtoF(charVal):
			return False
	return True

eyeColors = ['amb','blu','brn','gry','grn','hzl','oth']

def checkECL(key,record):
	value = getFieldValue(key,record)
	debugPrint('ecl '+value)
	if value not in eyeColors:
		return False
	return True

def checkPID(key,record):
	value = getFieldValue(key,record)
	debugPrint('pid '+value)
	if not isValidLength(9,value):
		return False
	for digitVal in value:
		if not isInRange('0','9',digitVal):
			return False
	return True

def validatePassportRecord(record):
	if not checkBYR('byr',record):
		return False
	if not checkIYR('iyr',record):
		return False
	if not checkEYR('eyr',record):
		return False
	if not checkHGT('hgt',record):
		return False
	if not checkHCL('hcl',record):
		return False
	if not checkECL('ecl',record):
		return False
	if not checkPID('pid',record):
		return False
	return True

inList = readFileOfStringsToList()
debugPrint(inList)
validPassportCount = 0
passportsWithAllFields = []
for record in inList:
	gotFields = True
	for reqField in requiredFields:
		if reqField not in record:
			gotFields = False
	if gotFields:
		validPassportCount += 1
		passportsWithAllFields.append(record)

debugPrint('validPassportCount '+str(validPassportCount))
debugPrint('passportsWithAllFields'+str(passportsWithAllFields))
print('count of passportsWithAllFields',len(passportsWithAllFields))
passportsWithFieldsValidated = 0
for record in passportsWithAllFields:
	if validatePassportRecord(record):
		passportsWithFieldsValidated += 1

print('passportsWithFieldsValidated',passportsWithFieldsValidated)
