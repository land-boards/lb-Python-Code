import mysql.connector
# https://www.youtube.com/watch?v=jA1GO6g_Rw0&t=7s

mydb = mysql.connector.connect(user='test',
	password='test',
	database="mylbinv",
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM parts")
myList = mycursor.fetchall()
for line in myList:
	print (line)
