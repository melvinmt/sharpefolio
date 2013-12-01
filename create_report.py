import sqlite3
from datetime import date, timedelta
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

reports_collection = report_mapper.find_all()

ratio_calc = calc.Ratio()

for report in reports_collection:
	# Report date range
	start_date = date(report.year, report.month, report.day)
	end_date   = start_date + timedelta(days=report.duration)

	stocks_collection = stock_mapper.find_all()
	for stock in stocks_collection:
		prices_collection = price_mapper.find_by_stock_id_in_range(stock.id, start_date, end_date)
		prices = [price.closing_price for price in prices_collection]
		sharpe = ratio_calc.sharpe(prices)
		print 'generating report %d for %s (%d-%d-%d): %f' % (report.id, stock.symbol, report.year, report.month, report.day, sharpe)
		ratio = reports.Ratio(stock.id, report.id, sharpe)
		ratio_mapper.insert(ratio)
