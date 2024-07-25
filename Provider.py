from datetime import datetime
import requests
import pandas as pd
import traceback
import time

class Provider:
	def __init__(self, settings):
		self.settings = settings
		self.session = None
		# self.last_day = str(datetime.now().date())
		self.last_day = '2023-10-11'

	def get_session(self):
		if not self.session: self.session = requests.Session()

	def close_session(self):
		if self.session:
			self.session.close()
			self.session = None

	def get_data(self):
		self.get_session()
		symbol_api_data = self.session.get(self.settings['symbol_url'], headers=self.settings['headers']).json()
		symbol_list = symbol_api_data['data']['table']['rows']
		print(len(symbol_list))
		now = time.time()
		data_dict = {}
		for symbol_data in symbol_list:
		# for symbol_data in ('AAPL', 'GOOG'):
			symbol = symbol_data['symbol']
			# symbol = symbol_data
			while True:
				try:
					symbol_price_api_data = self.session.get(self.settings['symbol_price_url'].format(symbol=symbol.replace('/', '%25sl%25'), last_day=self.last_day), headers=self.settings['headers'], timeout=5, stream=True).json()
					time.sleep(0.2)
					break
				except:
					# print(traceback.format_exc())
					print('重新連線')
					self.close_session()
					time.sleep(5)
					self.get_session()
					continue

			if symbol_price_api_data['status']['rCode'] != 200: continue
			symbol_price_list = symbol_price_api_data['data']['tradesTable']
			if not symbol_price_list: continue
			symbol_price_list = symbol_price_list.get('rows', None)
			for symbol_price_data in symbol_price_list:
				symbol_price_data['stock_id'] = symbol
				symbol_price_data['date'] = f"{symbol_price_data['date'][-4:]}/{symbol_price_data['date'][:5]}"
				for column in ('close', 'open', 'high', 'low',):
					symbol_price_data[column] = symbol_price_data[column].replace('$', '')
				symbol_price_data['volume'] = symbol_price_data['volume'].replace('N/A', '0')
			symbol_price_list.sort(key=lambda x: x['date'])
			data_dict[symbol] = pd.DataFrame(symbol_price_list)[['date', 'stock_id', 'close', 'open', 'high', 'low', 'volume']]
			print(f'\r{symbol} {time.time()-now}', end='')

		self.session.close()
		print('')
		df = pd.DataFrame()
		for symbol, stock_df in data_dict.items():
			df = df._append(stock_df)
			# df = pd.concat([df, stock_df], axis=0)
			print(f'\rdf {symbol} {time.time() - now}', end='')
		print('')
		print('總時間 ', time.time()-now)
		# print(df.reset_index(drop=True))
		df.to_csv('nasdaq.csv', encoding = 'utf-8', index = False)

			# for symbol_price_data in symbol_price_list:
			# 	symbol_price_data['stock_id'] = symbol.replace('%25sl%25', '/')

	def apply_sql(self, row):
		pass





