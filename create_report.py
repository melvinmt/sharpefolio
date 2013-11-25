import sqlite3
from datetime import date
from sharpefolio import stocks
from sharpefolio import reports
from sharpefolio import calc

connection = sqlite3.connect('test.sqlite')
connection.row_factory = sqlite3.Row

# Set up stock mapper
stock_repository = stocks.StockSqliteRepository(connection)
stock_mapper = stocks.StockMapper(stock_repository)

# Set up price mapper
price_repository = stocks.PriceSqliteRepository(connection)
price_mapper = stocks.PriceMapper(price_repository)

# Set up report mapper
report_repository = reports.ReportSqliteRepository(connection)
report_mapper = reports.ReportMapper(report_repository)

# Set up ratio mapper
ratio_repository = reports.RatioSqliteRepository(connection)
ratio_mapper = reports.RatioMapper(ratio_repository)

# Report date range
start_date = date(2013, 10, 1)
end_date   = date(2013, 10, 31)

report = reports.Report(start_date.year, start_date.month, start_date.day, (end_date - start_date).days, 'sharpe-v1.0-beta')
# Pretend we got this from the database
report._id = 1

stock = stock_mapper.find_by_symbol('AAPL')
prices_collection = price_mapper.find_by_stock_id_in_range(stock.id, start_date, end_date)

prices = [price.closing_price for price in prices_collection]

ratio_calc = calc.Ratio()
sharpe = ratio_calc.sharpe(prices)
sortino = ratio_calc.sortino(prices)

ratio = reports.Ratio(stock.id, report.id, sharpe)
ratio_mapper.insert(ratio)
