a='123'
a.isnumeric()
#True

b='a12'
b.isnumeric()
#False

def isInRange(lower,upper,val):
	# Returns True if val is in the range from lower to upper
	# Return False otherwise
	return lower <= val <= upper

def isValidLength(expectedLength,strToCheck):
	# returns True if the strToCheck length is expectedLength
	# Return False otherwise
	return len(strToCheck) == expectedLength
