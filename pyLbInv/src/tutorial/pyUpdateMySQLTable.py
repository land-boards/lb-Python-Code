import mysql.connector
# https://www.youtube.com/watch?v=W321PFPLcHk

mydb = mysql.connector.connect(user='test',
	password='test',
	database="mylbinv",
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
# get the boards where the qty is below some threshold
sql = "UPDATE parts SET qtyOnHand = 8 WHERE partID = 'ESP-BKOUT'"
mycursor.execute(sql)
mydb.commit()
