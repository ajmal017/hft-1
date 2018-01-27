import MySQLdb

class db(object):

	def __init__(self):
		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
		                     user="root",         # your username
		                     passwd="",  # your password
		                     db="trader")        # name of the data base

		self.cur = self.db.cursor()

	def select(self,query):
		result = self.cur.execute(query)
		for row in result.fetchall():
			print row[0]

	def insert_new_price(self,data,exchange):
		for d in data:
			for key, value in d.iteritems():
				result = self.cur.execute("INSERT INTO LastPrice (_ts,price,pair,exchange) VALUES (%s,%s,%s,%s);",(str(value["timestamp"]),str(value["price"]),value["pair"],exchange))
				self.db.commit()

	def close(self):
		self.db.close()