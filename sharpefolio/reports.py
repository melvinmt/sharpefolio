import datetime
import MySQLdb
import datamapper as dm

class Report(object):
	def __init__(self, date, duration, formula, id=None):
		self.id = id
		self.date = date
		self.duration = duration
		self.formula = formula

	def start_date(self):
		start_date = self._date
		weekdays = 0;
		while weekdays < self._duration:
			start_date -= datetime.timedelta(days=1)
			if start_date.weekday() < 5:
				weekdays += 1

		return start_date

class ReportMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

	def find_all(self):
		return self._repository.find_all()

class ReportMysqlRepository(dm.MysqlRepository):
	def insert(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `reports`\
			(`date`, `duration`, `formula`)\
			VALUES(%s, %s, %s)',
			(model.date, model.duration, model.formula)
		)
		self._database.commit()
		model._id = cursor.lastrowid

	def find_all(self):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `reports`')
		return dm.Collection(Report, cursor, self._datamap)

	def _datamap(self, data):
		data['date'] = datetime.datetime.strptime("%s" % data['date'], "%Y-%m-%d").date()
		return data

class Ratio(object):
	def __init__(self, stock_id, report_id, ratio, id = None):
		self._id = id
		self.stock_id = stock_id
		self.report_id = report_id
		self.ratio = ratio

class RatioMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

class RatioSqliteRepository(dm.SqliteRepository):
	def insert(self, model):
		self._database.execute('\
			INSERT INTO `ratios`\
			(`stock_id`, `report_id`, `ratio`)\
			VALUES(?, ?, ?)',
			(model.stock_id, model.report_id, model.ratio)
		)
		self._database.commit()

class RatioMysqlRepository(dm.MysqlRepository):
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
	def __init__(self, report_id, n_stocks=4, check_correlation=False, distribution='even', id=None):
		self.id = id
		self.report_id = report_id
		self.n_stocks = n_stocks
		self.check_correlation = check_correlation
		self.distribution = distribution

class RecipeMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

class RecipeMysqlRepository(dm.MysqlRepository):
	def insert(self, model):
		self._database.execute('\
			INSERT INTO `recipes`\
			(`report_id`, `n_stocks`, `check_correlation`, `distribution`)\
			VALUES(?, ?, ?, ?)',
			(model.report_id, model.n_stocks, model.check_correlation, model.distribution)
		)
		self._database.commit()

class Pick(object):
	def __init__(self, recipe_id, stock_id, gain, weight, id=None):
		self.id = id
		self.recipe_id = recipe_id
		self.stock_id = stock_id
		self.gain = gain
		self.weight = weight

class PickMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

class PickMysqlRepository(dm.MysqlRepository):
	def insert(self, model):
		self._database.execute('\
			INSERT INTO `picks`\
			(`recipe_id`, `stock_id`, `gain`, `weight`)\
			VALUES(?, ?, ?, ?)',
			(model.recipe_id, model.stock_id, model.gain, model.weight)
		)
		self._database.commit()
