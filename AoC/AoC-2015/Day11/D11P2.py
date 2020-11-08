# D11P1

password = 'hepxxzaa'

def checkThreeStraightIncreasing(inStr):
	for theCharOffset in range(len(inStr)-2):
		if  ((ord(inStr[theCharOffset+0])+0) == (ord(inStr[theCharOffset+1])-1)) \
		and ((ord(inStr[theCharOffset+1])+0) == (ord(inStr[theCharOffset+2])-1)):
			#print("Passed three consec")
			return True
	#print("Failed three consec")
	return False
	
def countPairs(inStr):
	pairCount = 0
	theCharOffset = 0
	while theCharOffset < (len(inStr)-1):
		if inStr[theCharOffset] == (inStr[theCharOffset+1]):
			pairCount += 1
			theCharOffset += 2
		else:
			theCharOffset += 1
	if pairCount >= 2:
		#print("Passed pair count > 2")
		return True
	else:
		#print("Failed pair count > 2")
		return False

def checkIllegalChars(inStr):
	if 'i' in inStr:
		return False
	if 'o' in inStr:
		return False
	if 'l' in inStr:
		return False
	return True
	
def checkString(inStr):
	#print("\nChecking",inStr)
	if not checkThreeStraightIncreasing(inStr):
		return False
	if not countPairs(inStr):
		return False
	if not checkIllegalChars(inStr):
		return False
	else:
		return True
	
def findColToInc(oldPassword):
	currentCol = 7
	while oldPassword[currentCol] == 'z':
		currentCol -= 1
	return currentCol

def incCol(col, password):
	newPassword = ''
	newPassword = password[0:col]
	charToInc = password[col]
	#print("incrementing char",charToInc)
	calCharToInc = ord(charToInc)
	calCharToInc += 1
	newChar = chr(calCharToInc)
	#print("character after increment",newChar)
	newPassword += newChar
	for colFill in range(col+1,8):
		newPassword += 'a'
	return newPassword

def newPassword(oldPassword):
	col = findColToInc(oldPassword)
	newPassword = incCol(col, oldPassword)
	return newPassword

if checkString('hijklmmn'):
	print("hijklmmn Passed")
else:
	print("hijklmmn Failed")
	
if checkString('abbceffg'):
	print("abbceffg Passed")
else:
	print("abbceffg Failed")
	
if checkString('abbcegjk'):
	print("abbcegjk Passed")
else:
	print("abbcegjk Failed")

if checkString('hepxcrrq'):
	print("hepxcrrq Passed")
else:
	print("hepxcrrq Failed")

while not checkString(password):
	#print("Checking",password)
	password = newPassword(password)
	
print("New password",password)
