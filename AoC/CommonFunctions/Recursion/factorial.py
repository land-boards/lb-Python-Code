#!/usr/bin/env python

# import sys
# sys.setrecursionlimit(5000)

# factorial example of recursion
def factorial(n):
	print('factorial called with n =',n)
	if n == 1:
		print(' reached 1')
		return 1
	else:
		print(' recursively call factorial, n =',n) 
		return n * factorial(n-1)

print(factorial(3))
