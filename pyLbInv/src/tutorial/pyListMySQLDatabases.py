import mysql.connector
# https://www.youtube.com/watch?v=-YU36D7oTLA

mydb = mysql.connector.connect(user='test',
	password='test',
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
for db in mycursor:
	print db
	