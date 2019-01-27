import mysql.connector
# https://www.youtube.com/watch?v=bYbIDccyW8Q

mydb = mysql.connector.connect(user='test',
	password='test',
	database="mylbinv",
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
sql = "DROP TABLE parts"
mycursor.execute(sql)
mydb.commit()
