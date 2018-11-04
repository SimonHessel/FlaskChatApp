import mysql.connector
class Database:
	def __init__(self):
		self.host = "localhost"
		self.user = "user"
		self.passwd = "password"
		self.database = "projekt"

		self.con = None

		self.setCon()

	def get(self,sql_command,params=None):
		if self.con == None:
			self.setCon();
			return [[0]]
		cur = self.con.cursor()
		cur.execute(sql_command,params)
		result = cur.fetchall()
		cur.close()
		return result

	def set(self,sql_command,params=None):
		if self.con == None:
			self.setCon();
			return ''
		cur = self.con.cursor()
		cur.execute(sql_command,params)
		self.con.commit()
		cur.close()
		return 'successful'

	def setCon(self):
		try:
			self.con = mysql.connector.connect(host=self.host, user=self.user,passwd=self.passwd,database=self.database)
		except mysql.connector.Error as err:
			print(err)
