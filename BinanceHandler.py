import json
import time
from SheetsHandler import sheets
from ApiHandler import api
from DatabaseHandler import db

class binance(object):

	def __init__(self):
		self.pairs = [['BTCUSDT'],['VENBTC'],['TRXBTC'],['ETHBTC'],['CNDBTC'],['ETHUSDT'],['TRXETH'],['EOSBTC'],['BNBBTC'],['VENETH'],['ELFBTC'],['EOSETH'],['WTCBTC'],['ICXBTC'],['XRPBTC'],['VIBEBTC'],['CNDETH'],['NEOBTC'],['BNBUSDT'],['XVGBTC'],['NEOUSDT']]
		
		m = api().binance_public()
		self.mp = json.loads(m.text)

		self.summary_prices = [time.time()]
		self.summary_headers = ["timestamp"]

		self.data = {}

	def write(self):
		for d in self.mp:
			for p in self.pairs:
				if (d['symbol'] in p):
					self.summary_headers.append(d['symbol'])
					self.summary_prices.append(d['price'])

					self.data[d['symbol']] = {"price":d['price'],"timestamp":time.time(),"pair":d['symbol']}

		sheets().write_summary_headers(self.summary_headers,'Binance')
		sheets().write_summary_data(self.summary_prices,'Binance')
		db().insert_new_price([self.data],'binance')