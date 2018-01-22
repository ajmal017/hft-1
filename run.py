import json
import time
from SheetsHandler import sheets
from ConnectionHandler import connect

# The below commented out bit finds all the active tradepairs

# t = requests.get('https://www.cryptopia.co.nz/api/GetTradePairs')
# tp = json.loads(t.text)

# active_pairs = []

# for trade_pair in tp['Data']:
# 	if trade_pair['Status'] == 'OK' and trade_pair['BaseSymbol'] == 'BTC':
# 		active_pairs.append(trade_pair['Label'])



pairs = [['ETN/BTC'],['BTC/USDT'],['ETH/BTC'],['KBR/BTC'],['LUX/BTC'],['ZCL/BTC'],['LTC/BTC'],['XVG/BTC'],['ETN/USDT'],['PROC/BTC'],['DOGE/BTC'],['CAPP/BTC'],['XBY/BTC'],['LINDA/BTC'],['R/BTC'],['NEO/BTC'],['RDD/BTC'],['BWK/BTC'],['DOT/BTC'],['GBX/BTC'],['DBIX/BTC'],['BTX/BTC'],['NMS/BTC'],['BCH/BTC'],['SAGA/BTC'],['POLL/BTC'],['ETH/USDT'],['CRC/BTC'],['MINT/BTC'],['ORME/BTC'],['VOISE/BTC'],['ETC/BTC'],['BTG/BTC'],['SPANK/BTC'],['ADST/BTC']]

m = connect().requests_retry_session().get('https://www.cryptopia.co.nz/api/GetMarkets/BTC/1')
mp = json.loads(m.text)

s = []
detailed_prices = []
summary_prices = [time.time()]
summary_headers = ["timestamp"]

for d in mp['Data']:
	for p in pairs:
		if (d['Label'] in p):
			s.append(d['Label'])
			array = [
				d['Label'],
				time.time(),
				d['SellVolume'],
				d['Volume'],
				d['SellBaseVolume'],
				d['LastPrice'],
				d['TradePairId'],
				d['High'],
				d['BidPrice'],
				d['Low'],
				d['BuyBaseVolume'],
				d['Close'],
				d['BaseVolume'],
				d['Open'],
				d['AskPrice'],
				d['Change'],
				d['BuyVolume']
			]
			detailed_prices.append(array)
			summary_headers.append(d['Label'])
			summary_prices.append(d['LastPrice'])

sheets().check_and_build_sheets(pairs)
# sheets().write_detailed_headers(pairs)
sheets().write_summary_headers(summary_headers)
sheets().insert_empty_rows()
sheets().write_summary_data(summary_prices)
# sheets().write_detailed_data(detailed_prices)