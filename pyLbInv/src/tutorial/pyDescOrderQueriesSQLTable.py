import mysql.connector
# https://www.youtube.com/watch?v=Op2b5XibDgk

mydb = mysql.connector.connect(user='test',
	password='test',
	database="mylbinv",
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
sql = "SELECT * FROM parts ORDER BY partID DESC"
mycursor.execute(sql)
myresult = mycursor.fetchall()
for result in myresult:
	print (result)
	