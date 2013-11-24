import sqlite3
from sharpefolio import stocks

connection = sqlite3.connect('test.sqlite')
connection.row_factory = sqlite3.Row

# Set up stock mapper
stock_repository = stocks.StockSqliteRepository(connection)
stock_mapper = stocks.StockMapper(stock_repository)

files = ["tmp/nasdaqlisted.txt", "tmp/otherlisted.txt"]

for filename in files:
	with open(filename, "r") as f:
		f.readline()
		for line in f:
			parts = line.split("|")
			if len(parts[1]) != 0:
				symbol = parts[0]
				company = parts[1]
				stock = stocks.Stock(symbol, company)
				try:
					stock_mapper.insert(stock)
				except sqlite3.IntegrityError, e:
					print 'Stock already exists:', stock.symbol
				else:
					print 'Found new stock:', stock.symbol
