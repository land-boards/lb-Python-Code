# https://www.youtube.com/watch?v=wMNrSM5RFMc

def factorial(val):
	print("called factorial with val :",val)
	if val < 0:			# error case
		return -1
	elif val < 2:		# base case
		return 1
	else:
		print("returning :",(val * factorial(val-1)))
		return val * factorial(val-1)

print(factorial(5))
