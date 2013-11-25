import sqlite3
from sharpefolio import stocks
from sharpefolio import calc

connection = sqlite3.connect('test.sqlite')
connection.row_factory = sqlite3.Row

# Set up stock mapper
stock_repository = stocks.StockSqliteRepository(connection)
stock_mapper = stocks.StockMapper(stock_repository)

# Set up price mapper
price_repository = stocks.PriceSqliteRepository(connection)
price_mapper = stocks.PriceMapper(price_repository)

stock = stock_mapper.find_by_symbol('ABCB')
prices_collection = price_mapper.find_by_stock_id(stock.id)
prices = [price.closing_price for price in prices_collection]

ratio = calc.Ratio()
sharpe = ratio.sharpe(prices)
sortino = ratio.sortino(prices)
print 'sharpe:', sharpe, 'sortino:', sortino
