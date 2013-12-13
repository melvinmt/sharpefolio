from sharpefolio import stocks
from sharpefolio import reports
from sharpefolio import calc
from datetime import date, timedelta
import sys
import MySQLdb

connection = MySQLdb.connect(
	host="127.0.0.1",
	user="vagrant",
	passwd="vagrant",
	db="sharpefolio"
)

# Set up stock mapper
stock_repository = stocks.StockMysqlRepository(connection)
stock_mapper = stocks.StockMapper(stock_repository)

# Set up price mapper
price_repository = stocks.PriceMysqlRepository(connection)
price_mapper = stocks.PriceMapper(price_repository)

# Set up report mapper
report_repository = reports.ReportMysqlRepository(connection)
report_mapper = reports.ReportMapper(report_repository)

# Set up ratio mapper
ratio_repository = reports.RatioMysqlRepository(connection)
ratio_mapper = reports.RatioMapper(ratio_repository)

# Set up pick mapper
pick_repository = reports.PickMysqlRepository(connection)
pick_mapper = reports.PickMapper(pick_repository)

# Set up recipe mapper
recipe_repository = reports.RecipeMysqlRepository(connection)
recipe_mapper = reports.RecipeMapper(recipe_repository)

reports_collection = report_mapper.find_all()

combos = {
			'n_stocks': [4, 5, 6, 7, 8],
			'check_correlation': [True, False],
			'distribution': ['even', 'ratio']
		}

def recipes_for_combos(combos, report):
	recipes = []
	for n_stocks in combos['n_stocks']:
		for check_correlation in combos['n_stocks']:
			for distribution in combos['distribution']:
				recipe = reports.Recipe(report.id, n_stocks, check_correlation, distribution)
				recipes.append(recipe)
	return recipes


def picks_with_least_correlation(report, recipe):

	start_date = date(report.date.year, report.date.month, report.date.day)
	end_date = start_date + timedelta(days=report.duration)

	top_ratios = ratio_mapper.find_highest_ratio(recipe.report_id, recipe.n_stocks)

	stocks = [stock_mapper.find_by_id(ratio.stock_id) for ratio in top_ratios]

	stock_prices = {}
	for stock in stocks:
		stock_prices[stock.symbol] = price_mapper.find_by_stock_id_in_range(stock.id, start_date, end_date)

	picker = calc.InvertedCorrelationPicker(stock_prices)
	return picker.pick(recipe.n_stocks)

def picks_with_highest_ratio(report, recipe):

	picks = []

	highest_ratios = ratio_mapper.find_highest_ratio(report.id, recipe.n_stocks)

	picks = [stock_mapper.find_by_id(ratio.stock_id).symbol for ratio in highest_ratios]

	return picks

def distribute_picks_evenly(picks):

	picks = []

	return picks


def distribute_picks_by_ratio(picks):

	picks = []

	return picks

def calc_gain_for_date(stock, today):

	price_today = price_mapper.find_by_stock_id_in_range(stock.id, start_date=today, end_date=today)
	yesterday = today - timedelta(days=1)
	price_yesterday = price_mapper.find_by_stock_id_in_range(stock.id, start_date=yesterday, end_date=yesterday)

	gain = price_today - price_yesterday

	return gain

for report in reports_collection:

	start_date = date(report.date.year, report.date.month, report.date.day)
	end_date   = start_date + timedelta(days=report.duration)

	for recipe in recipes_for_combos(combos, report):
		# recipe_mapper.insert(recipe)

		# Check correlation of stocks
		# if recipe.check_correlation == True:
		# 	picks = picks_with_least_correlation(recipe)
		# else:
		# 	picks = picks_with_highest_ratio(recipe)

		picks = picks_with_highest_ratio(report, recipe)

		print "highest ratio picks:", picks

		picks = picks_with_least_correlation(report, recipe)

		print "least correlation picks:", picks

		sys.exit()

		# Distribute stocks
		if recipe.distribution == 'ratio':
			picks = distribute_picks_by_ratio(picks)
		else:
			picks = distribute_picks_evenly(picks)

		# Store picks in DB
		for symbol in picks.keys():
			stock = stock_mapper.find_by_symbol(symbol)
			
			gain = calc_gain_for_date(stock, start_date)
			weight = picks[symbol]

			pick = reports.Pick(recipe.id, stock.id, gain, weight)
			pick_mapper.insert(pick)

