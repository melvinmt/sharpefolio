import numpy as np

class Ratio(object):
	'''
	all list parameters are expected to be an one dimensional
	list of nominal prices, e.g. [1,1.2,.3,10,.3,25]
	'''
	def sharpe(self, prices, benchmark = None):

		n = len(prices)
		benchmark = self._prepare_benchmark(benchmark, n)

		ret = np.diff(prices)
		b_ret = np.diff(benchmark)
		adj_ret = [a - b for a, b in zip(ret, b_ret)]

		std = np.std(ret)

		return self._get_ratio(adj_ret, std, n)

	def sortino(self, prices, benchmark = None):
		'''
		sortino is an adjusted sharpe ratio which only takes
		the standard deviation of negative returns into account
		'''
		n = len(prices)
		benchmark = self._prepare_benchmark(benchmark, n)

		ret = np.diff(prices)
		b_ret = np.diff(benchmark)
		adj_ret = [a - b for a, b in zip(ret, b_ret)]

		print "adj_ret", adj_ret

		neg_ret = [a for a in adj_ret if a < 0]

		print "neg_ret", neg_ret

		std = np.std(neg_ret)

		print "std", std

		return self._get_ratio(adj_ret, std, n)

	def _get_ratio(self, ret, std, n):

		avg = np.mean(ret)

		if std > 0:
			return avg * np.sqrt(n) / std
		else:
			return 0

	def _prepare_benchmark(self, benchmark, n):

		if benchmark == None:
			benchmark = np.zeros(n)
		if len(benchmark) != n:
			raise Exception("benchmark mismatch")

		return benchmark

r = Ratio()
prices = [1,1.2,.3,10,.3,25]
sharpe = r.sharpe(prices)
sortino = r.sortino(prices)
print "sharpe:", sharpe, "sortino:", sortino

