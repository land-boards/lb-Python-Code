import mysql.connector
# https://www.youtube.com/watch?v=OTzL0oH-ZGI

mydb = mysql.connector.connect(user='test',
	password='test',
	database="mylbinv",
	host='127.0.0.1',
	auth_plugin='mysql_native_password')

mycursor = mydb.cursor()
# get the boards where the qty is below some threshold
sql = "SELECT * FROM parts WHERE partID LIKE %s"
mycursor.execute(sql,("ESP%",))
myresult = mycursor.fetchall()
for tb in myresult:
	print (tb)
	