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
		start_date = self.date
		weekdays = 0;
		while weekdays < self.duration:
			start_date -= datetime.timedelta(days=1)
			if start_date.weekday() < 5:
				weekdays += 1

		return start_date

class ReportMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

	def find_all(self):
		return self._repository.find_all()

	def find_within_date(self, since_date, until_date):
		return self._repository.find_within_date(since_date, until_date)

	def find_until_date(self, until_date):
		return self._repository.find_until_date(until_date)

	def find_until_date_with_duration_and_formula(self, until_date, duration, formula):
		return self._repository.find_until_date_with_duration_and_formula(
			until_date, duration, formula
		)

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
		model.id = cursor.lastrowid

	def find_all(self):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `reports`')
		return dm.Collection(Report, cursor, self._datamap)

	def find_within_date(self, since_date, until_date):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `reports` WHERE `date` >= %s AND `date` <= %s ORDER BY `date` DESC', (since_date, until_date))
		return dm.Collection(Report, cursor, self._datamap)

	def find_until_date(self, until_date):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `reports` WHERE date <= %s', (until_date,))
		return dm.Collection(Report, cursor, self._datamap)

	def find_until_date_with_duration_and_formula(self, until_date, duration, formula):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `reports` WHERE date <= %s AND duration = %s AND formula = %s', 
			(until_date, duration, formula)
		)
		return dm.Collection(Report, cursor, self._datamap)

	def _datamap(self, data):
		data['date'] = datetime.datetime.strptime("%s" % data['date'], "%Y-%m-%d").date()
		return data

class Ratio(object):
	def __init__(self, stock_id, report_id, ratio, id = None):
		self.id = id
		self.stock_id = stock_id
		self.report_id = report_id
		self.ratio = ratio

	def __str__(self):
		return "stock_id: %d report_id: %d ratio: %d" % (self.stock_id, self.report_id, self.ratio)

class RatioMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

	def find_highest_ratio(self, report_id, limit):
		return self._repository.find_highest_ratio(report_id, limit)

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

	def find_highest_ratio(self, report_id, limit):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `ratios` WHERE report_id = %s ORDER BY ratio DESC LIMIT %s', (report_id, limit))
		return dm.Collection(Ratio, cursor)

class Recipe(object):
	def __init__(self, report_formula, report_duration, n_stocks=4, check_correlation=False, distribution='even', id=None):
		self.id = id
		self.n_stocks = n_stocks
		self.check_correlation = check_correlation
		self.distribution = distribution
		self.report_formula = report_formula
		self.report_duration = report_duration

class RecipeMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

class RecipeMysqlRepository(dm.MysqlRepository):
	def insert(self, model):
		cursor = self._database.cursor()
		# q = '\
		# 	INSERT INTO `recipes`\
		# 	(`n_stocks`, `check_correlation`, `distribution`,`report_duration`, `report_formula`)\
		# 	VALUES(%s, %s, %s, %s, %s)' % (model.n_stocks, int(model.check_correlation), model.distribution, model.report_duration, model.report_formula)
		# print q
		cursor.execute('\
			INSERT INTO `recipes`\
			(`n_stocks`, `check_correlation`, `distribution`,`report_duration`, `report_formula`)\
			VALUES(%s, %s, %s, %s, %s)',
			(model.n_stocks, int(model.check_correlation), model.distribution, model.report_duration, model.report_formula)
		)
		self._database.commit()
		model.id = cursor.lastrowid

class Pick(object):
	def __init__(self, recipe_id, report_id, stock_id, weight, id=None):
		self.id = id
		self.report_id = report_id
		self.recipe_id = recipe_id
		self.stock_id = stock_id
		self.weight = weight

class PickMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

class PickMysqlRepository(dm.MysqlRepository):
	def insert(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `picks`\
			(`recipe_id`, `report_id`, `stock_id`, `weight`)\
			VALUES(%s, %s, %s, %s, %s)',
			(model.recipe_id, model.report_id, model.stock_id, model.weight)
		)
		self._database.commit()
		model.id = cursor.lastrowid
