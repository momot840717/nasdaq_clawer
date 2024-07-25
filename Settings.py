settings = {
	'symbol_url': 'https://api.nasdaq.com/api/screener/stocks?tableonly=True&limit=999999&offset=0',
	'symbol_price_url': 'https://api.nasdaq.com/api/quote/{symbol}/historical?assetclass=stocks&fromdate=2015-01-01&limit=999999999&todate={last_day}',
	'headers': {
		'Referer': 'https://www.nasdaq.com/',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
	}

}