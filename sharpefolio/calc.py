import numpy as np
from itertools import combinations

class Ratio(object):
	'''
	all list parameters are expected to be an one dimensional
	list of nominal prices, e.g. [1,1.2,.3,10,.3,25]
	'''
	def __init__(self, prices, benchmark = None):
		self.prices = prices
		self.n = len(self.prices)
		self.benchmark = self._prepare_benchmark(benchmark)
		self.ret = np.diff(self.prices)
		self.b_ret = np.diff(self.benchmark)

	def sharpe(self):

		adj_ret = [a - b for a, b in zip(self.ret, self.b_ret)]
		std = np.std(self.ret)

		return self._get_info_ratio(adj_ret, std)

	def sortino(self):
		'''
		sortino is an adjusted ratio which only takes the 
		standard deviation of negative returns into account
		'''
		adj_ret = [a - b for a, b in zip(self.ret, self.b_ret)]
		neg_ret = [a for a in adj_ret if a < 0]

		neg_std = np.std(neg_ret)

		return self._get_info_ratio(adj_ret, neg_std)

	def _get_info_ratio(self, ret, std):

		avg = np.mean(ret)

		if std > 0.0001:
			return avg * np.sqrt(self.n) / std
		else:
			return 0

	def _prepare_benchmark(self, benchmark):

		if benchmark == None:
			benchmark = np.zeros(self.n)
		if len(benchmark) != self.n:
			raise Exception("benchmark mismatch")

		return benchmark

class InvertedCorrelationPicker(object):

	def __init__(self, stocks):

		'''
		stocks = {
				  "AAPL": [0.23, 0.24, 0.25, 0.26],
				  "TWTR": [-0.23, -0.24, -0.25, -0.26],
				  "FB"  : [0.23, 0.24, 0.25, 0.26],
				  "LNKD": [-0.23, -0.24, -0.25, -0.26],
				  "ZNGA": [0.23, 0.24, 0.25, 0.26],
				  "GRPN": [0.3, 0.29, 0.4, 0.23],
				  "IBM" : [0.23, 0.24, 0.25, 0.26],
				  "MSFT": [0.23, 0.24, 0.25, 0.26],
				  "GOOG": [0.23, 0.24, 0.25, 0.26],
				 }
		picker = InvertedCorrelationPicker(stocks)
		'''

		self.stocks = stocks

	def pick(self, portfolio_size=4):

		'''
		picker.pick(4)
		'''

		price_len = 0
		stocks_len = len(self.stocks)
		symbols = [symbol for symbol in self.stocks.keys()]

		# Determine depth of matrix
		for symbol in symbols:
			if len(self.stocks[symbol]) > price_len:
				price_len = len(self.stocks[symbol])

		if portfolio_size > price_len:
			# Pick everything!
			return symbols

		# Create an empty datastructure to hold the daily returns
		cov_data = np.zeros((price_len, stocks_len))

		# Grab the daily returns for those stocks and put them in cov index
		for i, symbol in enumerate(symbols):
			prices = self.stocks[symbol]
			# n = len(prices)
			# if n < price_len:
				# Forward fill
				# prices += prices[-1:]*(price_len-n)
			cov_data[:,i] = prices

		# Make a correlation matrix
		cormat = np.corrcoef(cov_data.transpose())

		# Create all possible combinations of the n top equites for the given portfolio size.
		portfolios = list(combinations(range(0, stocks_len), portfolio_size))

		# Add up all the correlations for each possible combination
		total_corr = [sum([cormat[x[0]][x[1]] for x in combinations(p, 2)]) for p in portfolios]

		# Find the portfolio with the smallest sum of correlations
		picks = [symbols[i] for i in portfolios[total_corr.index(np.nanmin(total_corr))]]

		return picks

