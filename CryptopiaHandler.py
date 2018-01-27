import json
import time
from SheetsHandler import sheets
from ApiHandler import api
from DatabaseHandler import db

class cryptopia(object):

	def __init__(self):
		self.pairs = [['BTC/USDT'],['ETN/BTC'],['ETH/BTC'],['KBR/BTC'],['LUX/BTC'],['ZCL/BTC'],['LTC/BTC'],['XVG/BTC'],['ETN/USDT'],['PROC/BTC'],['DOGE/BTC'],['CAPP/BTC'],['XBY/BTC'],['LINDA/BTC'],['R/BTC'],['NEO/BTC'],['RDD/BTC'],['BWK/BTC'],['DOT/BTC'],['GBX/BTC'],['DBIX/BTC'],['BTX/BTC'],['NMS/BTC'],['BCH/BTC'],['SAGA/BTC'],['POLL/BTC'],['ETH/USDT'],['CRC/BTC'],['MINT/BTC'],['ORME/BTC'],['VOISE/BTC'],['ETC/BTC'],['BTG/BTC'],['SPANK/BTC'],['ADST/BTC']]
		
		m = api().cryptopia_public()
		self.mp = json.loads(m.text)

		self.summary_prices = [time.time()]
		self.summary_headers = ["timestamp"]

		self.data = {}

	def write(self):
		for d in self.mp['Data']:
			for p in self.pairs:
				if (d['Label'] in p):
					self.summary_headers.append(d['Label'])
					self.summary_prices.append(d['LastPrice'])

					self.data[d['Label']] = {"price":d['LastPrice'],"timestamp":time.time(),"pair":d['Label']}

		sheets().write_summary_headers(self.summary_headers,'cryptopia')
		sheets().write_summary_data(self.summary_prices,'cryptopia')
		db().insert_new_price([self.data],'cryptopia')