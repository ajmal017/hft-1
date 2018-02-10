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
		print "Inserting new prices for "+exchange
		for d in data:
			for key, value in d.iteritems():
				previous_price = float(self.calculate_price_change(value["pair"],exchange))
				result = self.cur.execute("INSERT INTO LastPrice (_ts,price,pair,exchange,previous_price) VALUES (%s,%s,%s,%s,%s);",(str(value["timestamp"]),str(value["price"]),value["pair"],exchange,previous_price))
				self.db.commit()

	def calculate_price_change(self,pair,exchange):
		# print 'SELECT price FROM LastPrice WHERE id = ( SELECT max(id) FROM LastPrice WHERE 1=1 AND pair = "{p}" AND exchange = "{e}") AND pair = "{p}" AND exchange = "{e}";'.format(p=pair, e=exchange)
		self.cur.execute('SELECT price FROM LastPrice WHERE id = ( SELECT max(id) FROM LastPrice WHERE 1=1 AND pair = "{p}" AND exchange = "{e}") AND pair = "{p}" AND exchange = "{e}";'.format(p=pair, e=exchange))
		return self.cur.fetchone()[0]

	def close(self):
		self.db.close()