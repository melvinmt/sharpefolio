class Report(object):
	def __init__(self, year, month, day, duration, formula='sharpe-v1.0-beta', correlated=False, top_n_stocks=4):
		self._id = None
		self._year = year
		self._month = month
		self._day = day;
		self._duration = duration
		self._formula = formula
		self._correlated = correlated
		self._top_n_stocks = top_n_stocks

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

	@property
	def correlated(self):
		return self._correlated

	@property
	def top_n_stocks(self):
		return self._top_n_stocks

class ReportMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

	def find_all(self):
		return self._repository.find_all()

class ReportSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `reports`\
			(`year`, `month`, `day`, `duration`, `formula`, `correlated`, `top_n_stocks`)\
			VALUES(?, ?, ?, ?, ?)',
			(model.year, model.month, model.day, model.duration, model.formula, model.correlated, model.top_n_stocks)
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
			data['year'],
			data['month'],
			data['day'],
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

class Pick(object):
	def __init__(self, report_id, stock_id, gain, weight):
		self._id = None
		self._report_id = report_id
		self._stock_id = stock_id
		self._gain = gain
		self._weight = weight

	@property
	def id(self):
		return self._id

	@property
	def report_id(self):
		return self._report_id

	@property
	def stock_id(self):
		return self._stock_id

	@property
	def gain(self):
		return self._gain

	@property
	def weight(self):
		return self._weight
