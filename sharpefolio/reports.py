import datetime

class Report(object):
	def __init__(self, date, duration, formula='sharpe-v1.0-beta'):
		self._id = None
		self._date = date
		self._duration = duration
		self._formula = formula

	@property
	def id(self):
		return self._id

	@property
	def date(self):
		return self._date

	@property
	def duration(self):
		return self._duration

	@property
	def formula(self):
		return self._formula

class ReportMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

	def find_all(self):
		return self._repository.find_all()

class ReportMysqlRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `reports`\
			(`date`, `duration`, `formula`)\
			VALUES(%s, %s, %s)',
			(model.date, model.duration, model.formula)
		)
		model._id = cursor.lastrowid

	def find_all(self):
		cursor = self._database.execute('SELECT * FROM `reports`')
		return ReportCollection(cursor)

class ReportCollection:
	def __init__(self, reports):
		self._reports = reports

	def __iter__(self):
		self._reports.__iter__()
		return self;

	def next(self):
		next = self._reports.next()
		return self.build_model(next)

	def build_model(self, data):
		model = Report(
			datetime.datetime.strptime(data['date'], "%Y-%m-%d").date(),
			data['duration'],
			data['formula']
		)
		model._id = data['id']
		return model

class Ratio(object):
	def __init__(self, stock_id, report_id, ratio):
		self._id = None
		self._stock_id = stock_id
		self._report_id = report_id
		self._ratio = ratio;

	@property
	def id(self):
		return self._id

	@property
	def stock_id(self):
		return self._stock_id

	@property
	def report_id(self):
		return self._report_id

	@property
	def ratio(self):
		return self._ratio

class RatioMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

class RatioSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		self._database.execute('\
			INSERT INTO `ratios`\
			(`stock_id`, `report_id`, `ratio`)\
			VALUES(?, ?, ?)',
			(model.stock_id, model.report_id, model.ratio)
		)
		self._database.commit()

class RatioMysqlRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `ratios`\
			(`stock_id`, `report_id`, `ratio`)\
			VALUES(%s, %s, %s)',
			(model.stock_id, model.report_id, model.ratio)
		)
		self._database.commit()

class Recipe(object):

	def __init__(self, report_id, n_stocks=4, check_correlation=False, distribution='even'):
		self._id = None
		self._report_id = report_id
		self._n_stocks = n_stocks
		self._check_correlation = check_correlation
		self._distribution = distribution

	@property
	def id(self):
		return self._id

	@property
	def report_id(self):
		return self._report_id

	@property
	def n_stocks(self):
		return self._n_stocks

	@property
	def check_correlation(self):
		return self._check_correlation

	@property
	def distribution(self):
		return self._distribution


class RecipeMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

class RecipeSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		self._database.execute('\
			INSERT INTO `recipes`\
			(`report_id`, `n_stocks`, `check_correlation`, `distribution`)\
			VALUES(?, ?, ?, ?)',
			(model.report_id, model.n_stocks, model.check_correlation, model.distribution)
		)
		self._database.commit()

class Pick(object):
	def __init__(self, recipe_id, stock_id, gain, weight):
		self._id = None
		self._recipe_id = recipe_id
		self._stock_id = stock_id
		self._gain = gain
		self._weight = weight

	@property
	def id(self):
		return self._id

	@property
	def recipe_id(self):
		return self._recipe_id

	@property
	def stock_id(self):
		return self._stock_id

	@property
	def gain(self):
		return self._gain

	@property
	def weight(self):
		return self._weight

class PickMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

class PickSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		self._database.execute('\
			INSERT INTO `picks`\
			(`recipe_id`, `stock_id`, `gain`, `weight`)\
			VALUES(?, ?, ?, ?)',
			(model.recipe_id, model.stock_id, model.gain, model.weight)
		)
		self._database.commit()
