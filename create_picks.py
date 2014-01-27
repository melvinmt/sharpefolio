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

combos = {
			'n_stocks': [4, 5, 6, 7, 8],
			'check_correlation': [True, False],
			'distribution': ['even', 'ratio'],
			'report_duration': [5, 10, 15, 20, 25, 30],
			'report_formula': ['sharpe-v1.0-beta', 'sortino-v1.0-beta']
		}

def recipe_combos(combos):
	recipes = []
	for n_stocks in combos['n_stocks']:
		for check_correlation in combos['check_correlation']:
			for distribution in combos['distribution']:
				for report_duration in combos['report_duration']:
					for report_formula in combos['report_formula']:
						recipe = reports.Recipe(report_formula, report_duration, n_stocks, check_correlation, distribution)
						recipes.append(recipe)
						recipe_mapper.insert(recipe)
	return recipes

class Picker:

	def __init__(self, report, recipe):
		self.report = report
		self.recipe = recipe

		self.start_date = report.start_date()
		self.end_date = date(self.report.date.year, self.report.date.month, self.report.date.day)

	def _picks_with_least_correlation(self):

		top_ratios = ratio_mapper.find_highest_ratio(self.report.id, self.recipe.n_stocks)

		stock_prices = {}
		for ratio in top_ratios:
			stock_prices[ratio.stock_id] = price_mapper.find_by_stock_id_in_range(ratio.stock_id, self.start_date, self.end_date)

		picker = calc.InvertedCorrelationPicker(stock_prices)

		picked_stock_ids = picker.pick(self.recipe.n_stocks)

		picks = {}
		for picked_stock_id in picked_stock_ids:
			for ratio in top_ratios:
				if ratio.stock_id == picked_stock_id:
					stock = stock_mapper.find_by_id(ratio.stock_id)
					picks[stock.symbol] = ratio.ratio

		return picks

	def _picks_with_highest_ratio(self):
		picks = {}

		highest_ratios = ratio_mapper.find_highest_ratio(self.report.id, self.recipe.n_stocks)

		for ratio in highest_ratios:
			symbol = stock_mapper.find_by_id(ratio.stock_id).symbol
			picks[symbol] = ratio.ratio

		return picks

	def _distribute_picks_evenly(self, picks):

		n = len(picks)

		dist = {}
		for symbol in picks.keys():
			dist[symbol] = 1.0 / n

		return dist

	def _distribute_picks_by_ratio(self, picks):

		n = sum(picks.values())

		dist = {}
		for symbol in picks.keys():
			dist[symbol] = picks[symbol] / n

		return dist

	def create_picks(self):
		# Check correlation of stocks
		if self.recipe.check_correlation == True:
			picks = self._picks_with_least_correlation()
		else:
			picks = self._picks_with_highest_ratio()

		# Distribute stock_prices
		if recipe.distribution == 'ratio':
			dist = self._distribute_picks_by_ratio(picks)
		else:
			dist = self._distribute_picks_evenly(picks)

		# Store picks in DB
		for symbol in picks.keys():
			stock = stock_mapper.find_by_symbol(symbol)

			weight = dist[symbol]

			print "recipe_id:", self.recipe.id, "report_id:", report.id,  "stock_id:", stock.id, "weight:", weight

			pick = reports.Pick(self.recipe.id, self.report.id, stock.id, weight)
			pick_mapper.insert(pick)

last_date = price_mapper.find_last_date()

for recipe in recipe_combos(combos):

	reports_collection = report_mapper.find_until_date_with_duration_and_formula(
		last_date, recipe.report_duration, recipe.report_formula
	)

	for report in reports_collection:

		picker = Picker(report, recipe)
		picker.create_picks()

