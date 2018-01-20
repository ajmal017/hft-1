import json
import datetime
from SheetsHandler import sheets
from ConnectionHandler import connect

# The below commented out bit finds all the active tradepairs

# t = requests.get('https://www.cryptopia.co.nz/api/GetTradePairs')
# tp = json.loads(t.text)

# active_pairs = []

# for trade_pair in tp['Data']:
# 	if trade_pair['Status'] == 'OK' and trade_pair['BaseSymbol'] == 'BTC':
# 		active_pairs.append(trade_pair['Label'])



pairs = [['ADC/BTC'],['ADST/BTC'],['ALIS/BTC'],['ATMS/BTC'],['BPL/BTC'],['BTDX/BTC'],['CRC/BTC'],['CRM/BTC'],['DASH/BTC'],['DCR/BTC'],['DGB/BTC'],['DNR/BTC'],['DP/BTC'],['DRP/BTC'],['ECOB/BTC'],['EMC2/BTC'],['ETC/BTC'],['ETHD/BTC'],['GNT/BTC'],['HC/BTC'],['HOLD/BTC'],['KBR/BTC'],['KEK/BTC'],['KMD/BTC'],['MGO/BTC'],['MLITE/BTC'],['MOIN/BTC'],['MONK/BTC'],['MTNC/BTC'],['NET/BTC'],['NLC2/BTC'],['NOBL/BTC'],['NTRN/BTC'],['NVC/BTC'],['ODN/BTC'],['OPAL/BTC'],['OPC/BTC'],['PCC/BTC'],['PHR/BTC'],['PIRL/BTC'],['PLC/BTC'],['POT/BTC'],['PRL/BTC'],['SPANK/BTC'],['TOK/BTC'],['TRC/BTC'],['TTC/BTC'],['UBQ/BTC'],['UFR/BTC'],['UIS/BTC'],['UMO/BTC'],['UNO/BTC'],['VIVO/BTC'],['XEM/BTC'],['XPM/BTC'],['XZC/BTC'],['ZEC/BTC']]
# pairs = [['ADC/BTC'],['ADST/BTC']]

m = connect().requests_retry_session().get('https://www.cryptopia.co.nz/api/GetMarkets/BTC/1')
mp = json.loads(m.text)

s = []
prices = []

for d in mp['Data']:
	for p in pairs:
		if (d['Label'] in p):
			s.append(d['Label'])
			prices.append([d['Label'],str(datetime.datetime.now()),d['LastPrice']])

sheets().check_and_build_sheets(pairs)
sheets().write_headers(pairs)
sheets().insert_empty_rows(pairs)
sheets().write_data(prices)