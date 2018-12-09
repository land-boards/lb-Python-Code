# test globals

def testit():
	global val
	val = val + 1

val = 1
testit()
print val
