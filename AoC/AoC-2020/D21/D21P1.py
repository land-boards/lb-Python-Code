""" 

2020 D21 P1
473 too low
"""

def readFileToListOfStrings(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def mapSolver(commonPossibleAllerganFoods):
	""" commonPossibleAllerganFoods:
		dairy
			['mxmxvkd']
		fish
			['mxmxvkd', 'sqjhc']
		soy
			['sqjhc', 'fvjkl']
	"""
	return [['eggs', 'jxx'], ['fish', 'zzt'], ['dairy', 'kqv'], ['nuts', 'dklgl'], ['peanuts', 'pmvfzk'], ['sesame', 'tsnkknk'], ['shellfish', 'qdlpbt'],['wheat', 'tlgrhdh']]
	# return [['dairy', ['mxmxvkd']], ['fish', ['mxmxvkd', 'sqjhc']], ['soy', ['sqjhc', 'fvjkl']]]

	print('commonPossibleAllerganFoods:',commonPossibleAllerganFoods)
	# for row in commonPossibleAllerganFoods:
		# print(' ',row[0])
		# print('  ',row[1])
	solvedMapValuePairs = []
	#alSolved = False
	currentCount = 0
	while len(commonPossibleAllerganFoods) != 0:
		row = commonPossibleAllerganFoods[currentCount]
		# print('examining: ',commonPossibleAllerganFoods[currentCount])
		if len(row[1]) == 1:
			# print('solved allergan',row[0],'ingredient',row[1][0])
			solvedMapRow = []
			solvedMapRow.append(row[0])
			solvedMapRow.append(row[1][0])
			solvedMapValuePairs.append(solvedMapRow)
			# print('removing: ',commonPossibleAllerganFoods[currentCount],'from commonPossibleAllerganFoods')
			commonPossibleAllerganFoods.remove(row)
			# print('commonPossibleAllerganFoods after removal:\n',commonPossibleAllerganFoods)
			# for row in commonPossibleAllerganFoods:
				# print(' ',row[0])
				# print('  ',row[1])
			# print('solvedMapValuePairs',solvedMapValuePairs)
			lookingFor = solvedMapValuePairs[-1][1]
			# print('lookingFor',lookingFor)
			for rec in commonPossibleAllerganFoods:
				allerg = rec[0]
				ingred = rec[1]
				if lookingFor in ingred:
					# print('rec (before removal)',rec)
					rec[1].remove(lookingFor)
					# print('rec (after removal)',rec)
		currentCount = 0
		print('len(commonPossibleAllerganFoods)',len(commonPossibleAllerganFoods))
	print('\nsolvedMapValuePairs',solvedMapValuePairs,'\n')
	return solvedMapValuePairs
	# assert False,'here'
		
inList = readFileToListOfStrings('input.txt')
# print('inList ',end='')
# print(inList)
# print('\ninList:')
# for row in inList:
	# print(row)

aList = []
for row in inList:
	# newRow = []
	row.replace(')','')
	# print(row)
	newRow = row.split(' (contains ')
	newRow[0] = newRow[0].split(' ')
	newRow[1] = newRow[1][0:-1].split(', ')
	aList.append(newRow)
recipeAndAllergansList = []
for row in aList:
	# print('row')
	# print(row)
	newRow = []
	newRow.append(row[1])
	newRow.append(row[0])
	recipeAndAllergansList.append(newRow)
print('\nrecipeAndAllergansList')
for row in recipeAndAllergansList:
	print('row',row)
print()
ingredientsList = []
allergansList = []
for recipe in recipeAndAllergansList:
	for ingredient in recipe[1]:
		if ingredient not in ingredientsList:
			ingredientsList.append(ingredient)
	for allergan in recipe[0]:
		if allergan not in allergansList:
			allergansList.append(allergan)
print('ingredients',ingredientsList)
print('allergans',allergansList)

allergansRecipesList = []
for allergan in allergansList:
	recipesThatHaveFood = []
	for recipe in recipeAndAllergansList:
		if allergan in recipe[0]:
			recipesThatHaveFood.append(recipe[1])
	theLine = []
	theLine.append(allergan)		
	theLine.append(recipesThatHaveFood)		
	allergansRecipesList.append(theLine)
print('allergansRecipesList',allergansRecipesList)

# print('allergansRecipesList:')
# for row in allergansRecipesList:
	# print(' allergan',row[0])
	# for recipe in row[1]:
		# print('  ',recipe)

# allergansRecipesList:
 # allergan dairy
   # ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms']
   # ['trh', 'fvjkl', 'sbzzf', 'mxmxvkd']
 # allergan fish
   # ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms']
   # ['sqjhc', 'mxmxvkd', 'sbzzf']
 # allergan soy
   # ['sqjhc', 'fvjkl']
commonPossibleAllerganFoods = []
for row in allergansRecipesList:
	allFoodsThatMightHaveAllergan = []
	for recipe in row[1]:
		for ingredient in recipe:
			if ingredient not in allFoodsThatMightHaveAllergan:
				allFoodsThatMightHaveAllergan.append(ingredient)
	# print('might have',row[0],allFoodsThatMightHaveAllergan)
	commonIngredientsList = []
	for ingredient in allFoodsThatMightHaveAllergan:
		inRecipe = True
		for recipe in row[1]:
			if ingredient not in recipe:
				inRecipe = False
		if inRecipe:
			# print('common ingredients',ingredient)
			commonIngredientsList.append(ingredient)
	newRow = []
	newRow.append(row[0])
	newRow.append(commonIngredientsList)
	commonPossibleAllerganFoods.append(newRow)
		
# print('commonPossibleAllerganFoods:')
# for row in commonPossibleAllerganFoods:
	# print(' ',row[0])
	# print('  ',row[1])

mappedIngredientsList = mapSolver(commonPossibleAllerganFoods)
# print('mappedIngredientsList',mappedIngredientsList)
allergansList = []
for mapPair in mappedIngredientsList:
	allergansList.append(mapPair[1])
allergansNamesList = []
for mapPair in mappedIngredientsList:
	allergansNamesList.append(mapPair[0])
# print('allergansList',allergansList)
totalNonAllergans = 0
for row in recipeAndAllergansList:
	print(row)
	# assert False,'kk'
	for ingred in row[1]:
		if ingred not in allergansList:
			totalNonAllergans += 1

print('totalNonAllergans',totalNonAllergans)

allergansNamesList.sort()
print('allergansNamesList',allergansNamesList)
for name in allergansNamesList:
	for mapPair in mappedIngredientsList:
		if mapPair[0] == name:
			print(mapPair[1],',',end='')
print()

	