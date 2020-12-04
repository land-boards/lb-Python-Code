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
inList = readFileOfStringsToList()
print(inList)
validPassportCount = 0
for record in inList:
	gotFields = True
	for reqField in requiredFields:
		if reqField not in record:
			gotFields = False
	if gotFields:
		validPassportCount += 1

print('validPassportCount',validPassportCount)
