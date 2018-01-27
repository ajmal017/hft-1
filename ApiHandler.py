from ConnectionHandler import connect

class api(object):

	def __init__(self):
		pass

	def binance_public(self):
		b = connect().requests_retry_session().get('https://www.binance.com/api/v1/ticker/allPrices')
		return b

	def cryptopia_public(self):
		c = connect().requests_retry_session().get('https://www.cryptopia.co.nz/api/GetMarkets/')
		return c