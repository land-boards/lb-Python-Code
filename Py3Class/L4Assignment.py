number_of_values = 0
input_value = 0
sum_of_numbers = 0
while input_value != -1:
    number_read = eval(input("Enter a number, -1 to stop: "))
    if number_read == -1:
        break
    sum_of_numbers = sum_of_numbers + number_read
    number_of_values = number_of_values + 1
print ("Number of values ",number_of_values)
print ("Sum of numbers ",sum_of_numbers)
average_of_numbers = sum_of_numbers / number_of_values
print ("Average of numbers ",average_of_numbers)
