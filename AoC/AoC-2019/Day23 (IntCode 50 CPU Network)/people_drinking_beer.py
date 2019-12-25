#!/usr/bin/env python3

class Person:
  def __init__(self, person_number):
    self.person_number = person_number
    self.beers_had = 0

  def drink_beer(self):
    self.beers_had += 1

fifty = []

for i in range(50):
  fifty.append(Person(i))

for i in range(0, 50, 2):
  fifty[i].drink_beer()