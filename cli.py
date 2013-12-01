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

url = 'http://query.yahooapis.com/v1/public/yql?'
params = {'format': 'json', 'env': 'store://datatables.org/alltableswithkeys', 'q': None}
query = 'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%04d-%02d-1" and endDate = "%04d-%02d-1"'

stocks_collection = stock_mapper.find_all()
for stock in stocks_collection:
	for year in xrange(2012,2013+1):
		try:
			params['q'] = query % (stock.symbol, year, 1, year + 1, 1)
			result = urllib2.urlopen(url+urllib.urlencode(params))
			data = json.load(result)
		except urllib2.HTTPError, e:
			print 'HTTP Error:', e, url+urllib.urlencode(params)
			raise e
		else:
			if data['query']['results'] == None:
				print '(%d) skipping empty result %s for %s' % (stock.id, stock.symbol, year)
				continue

			for info in data['query']['results']['quote']:
				try:
					close = info['Adj_Close']
					date = datetime.datetime.strptime(info['date'], '%Y-%m-%d')
					day = date.day
					month = date.month
					price = stocks.Price(stock.id, year, month, day, close, 0)
					price_mapper.insert(price)
				except Exception, e:
					print '(%d) error inserting %s for %d (%s)' % (stock.id, stock.symbol, year, e)
					pass
				except urllib2.HTTPError, e:
					print '(%d) HTTP Error %s' % (stock.id, e)
					raise e
				else:
					print '(%d) successfully imported %s for %d-%d-%d' % (stock.id, stock.symbol, year, month, day)
