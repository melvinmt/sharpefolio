class Stock(object):
	def __init__(self, symbol, company):
		self._id = None
		self._symbol = symbol
		self._company = company

	@property
	def id(self):
		return self._id

	@property
	def symbol(self):
		return self._symbol

	@property
	def company(self):
		return self._company

class StockMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

	def find_by_symbol(self, symbol):
		return self._repository.find_by_symbol(symbol)

	def find_all(self):
		return self._repository.find_all()

class StockSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		self._database.execute('INSERT INTO `stocks` (`symbol`, `company`) VALUES(?, ?)', (model.symbol, model.company))
		self._database.commit()

	def find_by_symbol(self, symbol):
		cursor = self._database.execute('SELECT * FROM `stocks` WHERE `symbol` = ? LIMIT 1', (symbol,))
		result = cursor.fetchone()

		return self.build_model(result)

	def find_all(self):
		cursor = self._database.execute('SELECT * FROM `stocks`')
		return StockCollection(cursor)

	def build_model(self, data):
		if (data == None):
			return None

		model = Stock(data['symbol'], data['company'])
		model._id = data['id']

		return model;

class StockCollection:
	def __init__(self, stocks):
		self._stocks = stocks

	def __iter__(self):
		self._stocks.__iter__()
		return self;

	def next(self):
		next = self._stocks.next()
		return self.build_model(next)

	def build_model(self, data):
		model = Stock(data['symbol'], data['company'])
		model._id = data['id']
		return model;

class Price(object):
	def __init__(self, stock_id, year, month, day, closing_price, change):
		self._id = None
		self._stock_id = stock_id
		self._year = year
		self._month = month
		self._day = day
		self._closing_price = closing_price
		self._change = change

	@property
	def stock_id(self):
		return self._stock_id

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
	def closing_price(self):
		return self._closing_price

	@property
	def change(self):
		return self._change

class PriceMapper:
	def __init__(self, repository):
		self._repository = repository

	def insert(self, model):
		self._repository.insert(model)

	def find_by_stock_id(self, stock_id):
		return self._repository.find_by_stock_id(stock_id)

	def find_by_stock_id_in_range(self, stock_id, start_date, end_date):
		return self._repository.find_by_stock_id_in_range(stock_id, start_date, end_date)

class PriceSqliteRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		self._database.execute('\
			INSERT INTO `prices`\
			(`stock_id`, `year`, `month`, `day`, `closing_price`, `change`)\
			VALUES(?, ?, ?, ?, ?, ?)',
			(model.stock_id, model.year, model.month, model.day, model.closing_price, model.change)
		)
		self._database.commit()

	def find_by_stock_id(self, stock_id):
		cursor = self._database.execute('SELECT * FROM `prices` WHERE `stock_id` = ? ORDER BY `year` ASC, `month` ASC, `day` ASC', (stock_id,))
		return PriceCollection(cursor)

	def find_by_stock_id_in_range(self, stock_id, start_date, end_date):
		cursor = self._database.execute("\
			SELECT *, date(year || '-' || substr('00' || month, -2, 2) || '-' || substr('00' || day, -2, 2)) as `the_date`\
			FROM `prices`\
			WHERE `stock_id` = ?\
			AND `the_date` >= date(?)\
			AND `the_date` <= date(?)\
			ORDER BY `year` ASC, `month` ASC, `day` ASC", (stock_id, start_date.isoformat(), end_date.isoformat())
		)
		return PriceCollection(cursor)

class PriceCollection:
	def __init__(self, prices):
		self._prices = prices

	def __iter__(self):
		self._prices.__iter__()
		return self;

	def next(self):
		next = self._prices.next()
		return self.build_model(next)

	def build_model(self, data):
		model = Price(
			data['stock_id'],
			data['year'],
			data['month'],
			data['day'],
			data['closing_price'],
			data['change']
		)
		model._id = data['id']
		return model;
