# D04P1

def readFileOfStringsToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inLine = inLine.replace(' ',':')
			inList.append(inLine.split(':'))
	return inList

expectedFields = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
requiredFields = ['byr','iyr','eyr','hgt','hcl','ecl','pid']

def getFieldValue(key,record):
	for fieldOffset in range(len(record)):
		if record[fieldOffset] == key:
			return record[fieldOffset+1]
	print('key',key,end=' ')
	print('record',record)
	assert False,'unexpected field'

def checkBYR(key,record):
	value = getFieldValue(key,record)
	print('byr',value)
	year = int(value)
	if 1920 <= year <= 2002:
		return True
	else:
		return False

def checkIYR(key,record):
	value = getFieldValue(key,record)
	print('iyr',value)
	year = int(value)
	if 2010 <= year <= 2020:
		return True
	else:
		return False

def checkEYR(key,record):
	value = getFieldValue(key,record)
	print('eyr',value)
	year = int(value)
	if 2020 <= year <= 2030:
		return True
	else:
		return False

def checkHGT(key,record):
	value = getFieldValue(key,record)
	print('hgt',value)
	if 'cm' in value:
		if len(value) != 5:
			return False
		hgt = value[0:3]
		hgtNum = int(hgt)
		if 150 <= hgtNum <= 193:
			return True
		else:
			return False
	elif 'in' in value:
		if len(value) != 4:
			return False
		hgt = value[0:2]
		hgtNum = int(hgt)
		if 59 <= hgtNum <= 76:
			return True
		else:
			return False
	else:
		return False
	assert False,"no clue how I got here"

def check_0to9_AtoF(charVal):
	#print('check_0to9_AtoF',charVal)
	if 'a' <= charVal <= 'f':
		return True
	if '0' <= charVal <= '9':
		return True
	else:
		print('failed check_0to9_AtoF')
		return False
		
def checkHCL(key,record):
	value = getFieldValue(key,record)
	print('hcl',value)
	if value[0] != '#':
		return False
	if len(value) != 7:
		return False
	for charVal in value[1:]:
		if not check_0to9_AtoF(charVal):
			return False
	return True

eyeColors = ['amb','blu','brn','gry','grn','hzl','oth']

def checkECL(key,record):
	value = getFieldValue(key,record)
	print('ecl',value)
	if value not in eyeColors:
		return False
	return True

def checkPID(key,record):
	value = getFieldValue(key,record)
	print('pid',value)
	if len(value) != 9:
		return False
	for digitVal in value:
		if not ('0' <= digitVal <= '9'):
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
#print(inList)
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

#print('validPassportCount',validPassportCount)
print('passportsWithAllFields',passportsWithAllFields)
print('count',len(passportsWithAllFields))
passportsWithFieldsValidated = 0
for record in passportsWithAllFields:
	if validatePassportRecord(record):
		passportsWithFieldsValidated += 1

print('passportsWithFieldsValidated',passportsWithFieldsValidated)
