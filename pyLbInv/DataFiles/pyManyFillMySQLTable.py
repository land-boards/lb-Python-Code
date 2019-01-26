import mysql.connector
# https://www.youtube.com/watch?v=BfXhZDNlXy8

mydb = mysql.connector.connect(user='test',
	password='test',
	database="mylbinv",
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

print(mydb)
mycursor = mydb.cursor()
sqlFormula = "INSERT INTO parts (partID, qtyOnHand) VALUES (%s, %s)"

manyParts = [("ESP-BKOUT",8),
		("ESP-12E-01",8),
		("ESP-BKOUT", 8),]
mycursor.executemany(sqlFormula,manyParts)
mydb.commit()
