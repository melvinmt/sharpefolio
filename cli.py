import sqlite3
import urllib2
import urllib
import json
import datetime
from sharpefolio import stocks

connection = sqlite3.connect('test.sqlite')
connection.row_factory = sqlite3.Row

# Set up stock mapper
stock_repository = stocks.StockSqliteRepository(connection)
stock_mapper = stocks.StockMapper(stock_repository)

# Set up price mapper
price_repository = stocks.PriceSqliteRepository(connection)
price_mapper = stocks.PriceMapper(price_repository)

stock = stock_mapper.find_by_symbol('AAPL')
#price = stocks.Price(stock.id, 2013, 4, 20, 123.12, 12.1)

#price_mapper.insert(price)

url = 'http://query.yahooapis.com/v1/public/yql?'
params = {'format': 'json', 'env': 'store://datatables.org/alltableswithkeys', 'q': None}

query = 'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%04d-%02d-1" and endDate = "%04d-%02d-1"'

for year in xrange(2003,2013+1):
	for month in xrange(1, 12+1):
		if (month == 12):
			params['q'] = query % (stock.symbol, year, month, year + 1, 1)
		else:
			params['q'] = query % (stock.symbol, year, month, year, month + 1)
		result = urllib2.urlopen(url+urllib.urlencode(params))
		data = json.load(result)

		if data['query']['results'] == None:
			print 'skipping empty result'
			continue

		for info in data['query']['results']['quote']:
			close = info['Adj_Close']
			date = datetime.datetime.strptime(info['date'], '%Y-%m-%d')
			day = date.day
			try:
				print stock.symbol, 'for', year,month,day
				price = stocks.Price(stock.id, year, month, day, close, 0)
				price_mapper.insert(price)
			except Exception, e:
				print 'already inserted', stock.symbol, 'for', year,month,day
				pass
