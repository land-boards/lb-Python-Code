def change_value(value):
    """This function changes the value passed in to 1"""
    print ("Inside, value is:", value)
    value = 1
    print ("Inside, value is changed to:", value)

number = 5
print ("Outside, number is:", number)
change_value(number)
print ("Outside, number is now:", number)
