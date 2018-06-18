#!/usr/bin/env python

import json
import csv

with open('mfp-diaries.tsv', 'rb') as inputFile:
  reader = csv.reader(inputFile, delimiter='\t')

  with open('output.csv', 'wb') as outputFile:
    writer = csv.writer(outputFile)

    writer.writerow(['User', 'Date', 'Meal_Name', 'Meal_Number', 'Dish_Name', 'Dish_Number', 'Protein', 'Carbs', 'Fat'])

    for line in reader:
      userId, date, meals = line[0], line[1], json.loads(line[2])

      for meal in meals:

        for i, dish in enumerate(meal['dishes']):
          bogusDishNumber = i + 1
          allNutrition = {}

          for nutrition in dish['nutritions']:
            allNutrition[nutrition['name']] = nutrition['value']

          rowOut = [
            userId,
            date,
            meal['meal'].encode('ascii', 'ignore'),
            meal['sequence'],
            dish["name"].encode('ascii', 'ignore'),
            bogusDishNumber,
            allNutrition.get('Protein', '0'),
            allNutrition.get('Carbs', '0'),
            allNutrition.get('Fat', '0')
          ]

          writer.writerow(rowOut)
