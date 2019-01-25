cat1_lower, cat1_upper = 74,95
cat2_lower, cat2_upper = 96,110
cat3_lower, cat3_upper = 111,130
cat4_lower, cat4_upper = 131,155
cat5 = 156
wind_speed = eval(input("what is the wind speed: "))
if wind_speed < cat1_lower:
        print ("Not a hurricane")
elif wind_speed >= cat1_lower and wind_speed <= cat1_upper:
        print ("Category 1 hurricane")
elif wind_speed >= cat2_lower and wind_speed <= cat2_upper:
        print ("Category 2 hurricane")
elif wind_speed >= cat3_lower and wind_speed <= cat3_upper:
        print ("Category 3 hurricane")
elif wind_speed >= cat4_lower and wind_speed <= cat4_upper:
        print ("Category 4 hurricane")
elif wind_speed >= cat5:
        print ("Categor 5 hurricane")
else:
        print ("Invalid wind speed")
