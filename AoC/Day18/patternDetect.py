import random
import statistics

class MakeRepeatedListClass:
	def makeSingleRandomNumberList(self,headerLength):
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
		headerList = self.makeSingleRandomNumberList(headerLength)
		if debug_generateRandomishList:
			print 'headerList',headerList
		repeatList = self.makeSingleRandomNumberList(repeatLength)
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
		Singletons are guaranteed not to be in a repeated pattern if the data stream is long enough.
		Might be easier to skip the singleton values and start looking at the non-singleton values.
		
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
		"""Go through a list and find all of the items that are only in the list more than once.
		These items are candidate for being in the repeated pattern but they are not guaranteed to be in the repeated items list.
		
		:param: listToSearch
		:returns: list of items with multiple occurrences in the data
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
		
		:param valueToSearchForInList: The value to look for in the list
		:param listToSearch: The list to search
		"""
		listOffset = 0
		for item in listToSearch:
			if valueToSearchForInList == item:
				return listOffset
			listOffset += 1
			
	def makeFrequencyBins(self,listOfDuplicates,originalList):
		"""Create a dictionary with the number of times a number has been hit.
		Only run this for the high hitters.
		How do you know which ones are the high hitters? 
		May have to look at the data to figure it out.
		The most frequent numbers are the repeated ones if the pattern is long enough.
		Random enough data could have earlier hits of some of the data that is in the repeated pattern.
		List scan could be ob1 due to where the scan ends (test case doesn't take that into account)
		
		:param listOfDuplicates: The list of the items in the original list which are duplicates
		:param originalList: The original list itself
		:returns: dictionary of the frequency counts of each item
		"""
		debug_makeFrequencyBins = False
		freqBins = {}
		for dupListItem in listOfDuplicates:
			for origListItem in originalList:
				if dupListItem == origListItem:
					if dupListItem in freqBins:		# The item is in the list so increase the count
						freqBins[dupListItem] = freqBins[dupListItem] + 1
					else:							# The item is not in the list so add it to the list
						freqBins[dupListItem] = 1
		if debug_makeFrequencyBins:
			print 'makeFrequencyBins: freqBins',freqBins
		return freqBins

	def getMedianFreqCount(self,freqBinData):
		"""go through the dictionary with the bins of data pick the right value.
		Assume that the discriminator which removed the singletons did a pretty good job
		of filtering down the front end noise so that most of the values are around the median.
		
		:param freqBinData: Get the maximum frequency count
		:returns: the maximum value in the list of frequencies
		"""
		maxFreqValue = 0
		freqList = []
		for x, y in freqBinData.items():
			if freqBinData:
				print(x, y)
			freqList.append(y)
		medianFreq = statistics.median(freqList)
		return freqList[-1]
	
GeneratorClass = MakeRepeatedListClass()
randomishList = GeneratorClass.generateRandomishList(100,20,10)	# repeatCount, headerLength, repeatLength
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

maxHits = PatternDetectClass.getMaxFreqCount(freqBinResults)
print 'maximum bin size',maxHits
