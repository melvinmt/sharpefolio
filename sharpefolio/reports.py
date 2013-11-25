class Report(object):
	def __init__(self, year, month, day, duration, formula):
		self._id = None
		self._year = year
		self._month = month
		self._day = day;
		self._duration = duration
		self._formula = formula

	@property
	def id(self):
		return self._id

	@property
	def year(self):
		return self._year

	@property
	def month(self):
		return self._month

	@property
	def day(self):
		return self._day

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

class ReportSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		self._database.execute('\
			INSERT INTO `reports`\
			(`year`, `month`, `day`, `duration`, `formula`)\
			VALUES(?, ?, ?, ?, ?)',
			(model.year, model.month, model.day, model.duration, model.formula)
		)
		self._database.commit()

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
