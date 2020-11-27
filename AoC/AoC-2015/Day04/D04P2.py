# 2015 Day 4, Part 1
#
  
import hashlib 
  
hashInitStr = 'yzbqklnj'
hashNumber = 0
gotLeadingZeros = False
while not gotLeadingZeros:
	hashNumberString = str(hashNumber)
	hashStr = hashInitStr + hashNumberString

	res = bytes(hashStr, 'utf-8') 
	result = hashlib.md5(res) 
	  
	# printing the equivalent byte value. 
	resultStr = result.hexdigest()

	if resultStr[0:6] == '000000':
		print("Got 0's")
		print("The hexadecimal equivalent of hash is : ", end ="") 
		print(resultStr)
		gotLeadingZeros = True
		print('appended',hashNumber)
	hashNumber += 1