def convert_to_fahrenheit(temp_in_deg_c):
	return (9.0/5.0 * temp_in_deg_c + 32)
	
for temp in range(0,101,10):
	print ("deg F: ",temp,"deg C: ",convert_to_fahrenheit(temp))
	