import json
import time
from SheetsHandler import sheets
from ConnectionHandler import connect
from BinanceHandler import binance
from CryptopiaHandler import cryptopia

class crypto(object):

	def __init__(self):
		sheets().insert_empty_rows()
		# cryptopia().write()
		binance().write()

crypto()