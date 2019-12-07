# Generate Phase Signals
# Phase signals can be 0-4
# There are 5 positions
# Each position has to be 0-4 once only

from __future__ import print_function

def genTestVecs():
	vecsList = []
	for dig0 in range(0,5):
		print("dig0",dig0)
		for dig1 in range(0,5):
			if dig1!= dig0:
				for dig2 in range(0,5):
					if ((dig2 != dig1) and (dig2 != dig0)):
						for dig3 in range(0,5):
							if ((dig3 != dig2) and (dig3 != dig1) and (dig3 != dig0)):
								for dig4 in range(0,5):
									if ((dig4 != dig3) and (dig4 != dig2) and (dig4 != dig1) and (dig4 != dig0)):
										vecsList.append([dig0,dig1,dig2,dig3,dig4])	
	return(vecsList)
		
vecs = genTestVecs()
print("test vectors :",vecs)
