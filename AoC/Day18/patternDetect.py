import random

class MakeRepeatedListClass:
	def makeRandomNumberList(self,headerLength):
		"""Make a list of random numbers
		
		:param headerLength: number of values in the list to return
		:returns: list of random numbers
		"""
		headerList = []
		for x in xrange(headerLength):
			headerList.append(random.randint(1,99))
		return headerList

	def generateRandomishList(self,repeatCount,headerLength,repeatLength):
		"""
		:param repeatCount: count of the number of times to repeat the repeated data pattern
		:param headerLength: number of values in the non-repeated part of the list
		:param repeatLength: number of values in the repeated part of the list
		"""
		debug_generateRandomishList = True
		headerList = self.makeRandomNumberList(headerLength)
		if debug_generateRandomishList:
			print 'headerList',headerList
		repeatList = self.makeRandomNumberList(repeatLength)
		if debug_generateRandomishList:
			print 'repeatList',repeatList
		resultList = []
		resultList.extend(headerList)
		for x in xrange(repeatCount): 
			resultList.extend(repeatList)
		return resultList

class PatternDetectorClass:
	def getSingletonsInList(self,listToSearch):
		"""Go through a list and find all of the items that are only in the list once.
		
		:param: listToSearch
		:returns: list of singletons in the data
		"""
		singletonList = []
		multipleItemsList = []
		for item in listToSearch:
			if (item not in singletonList) and (item not in multipleItemsList):
				singletonList.append(item)
			elif item in singletonList:
				singletonList.remove(item)
				multipleItemsList.append(item)
		return singletonList

	def getMultiplesInList(self,listToSearch):
		"""Go through a list and find all of the items that are only in the list once.
		
		:param: listToSearch
		:returns: list of singletons in the data
		"""
		singletonList = []
		multipleItemsList = []
		for item in listToSearch:
			if (item not in singletonList) and (item not in multipleItemsList):
				singletonList.append(item)
			elif item in singletonList:
				singletonList.remove(item)
				multipleItemsList.append(item)
		return multipleItemsList

	def findOffsetInListToValue(self,valueToSearchForInList,listToSearch):
		"""Search a list and find the offset to the item
		
		:param valueToSearchForInList: The value to look for in the list`
		:param listToSearch: the list to search in
		"""
		listOffset = 0
		for item in listToSearch:
			if valueToSearchForInList == item:
				return listOffset
			listOffset += 1
			
	def makeFrequencyBins(self,listOfDuplicates,originalList):
		"""Create a dictionary with the number of times a number has been hit
		The most frequent numbers are the repeated ones if the pattern is long enough.
		List scan could be ob1 due to where the scan ends (test case doesn't take that into account)
		
		:returns: dictionary of the frequency counts of each item
		"""
		freqBins = {}
		for dupListItem in listOfDuplicates:
			for origListItem in originalList:
				if dupListItem == origListItem:
					if dupListItem in freqBins:		# The item is in the list so increase the count
						freqBins[dupListItem] = freqBins[dupListItem] + 1
					else:							# The item is not in the list so add it to the list
						freqBins[dupListItem] = 1
		return freqBins
	
GeneratorClass = MakeRepeatedListClass()
randomishList = GeneratorClass.generateRandomishList(6,20,10)	# repeatCount, headerLength, repeatLength
print randomishList

PatternDetectClass = PatternDetectorClass()
singletonValues = PatternDetectClass.getSingletonsInList(randomishList)
print 'singletonValues',singletonValues
lastSingletonValue = singletonValues[-1]
print 'lastSingletonValue',lastSingletonValue
offsetInListToLastSingleton = PatternDetectClass.findOffsetInListToValue(lastSingletonValue,randomishList)
print 'offset in the list to the last singleton',offsetInListToLastSingleton
provisionalOffsetToPattern = offsetInListToLastSingleton + 1
print 'the provisional offset to the repeated pattern is',provisionalOffsetToPattern

duplicatedValues = PatternDetectClass.getMultiplesInList(randomishList)
print 'duplicatedValues',duplicatedValues
provisionalRepeatedValuesCount = len(duplicatedValues)
print 'the provisional repeatedValuesCount',provisionalRepeatedValuesCount

# Use frequency bins for the 
freqBinResults = PatternDetectClass.makeFrequencyBins(duplicatedValues,randomishList)
print 'freqBinResults',freqBinResults

