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
		self.repository = repository

	def insert(self, model):
		self.repository.insert(model)

	def find_by_symbol(self, symbol):
		return self.repository.find_by_symbol(symbol)

class StockSqliteRepository:
	def __init__(self, database):
		self.database = database

	def insert(self, model):
		self.database.execute('INSERT INTO `stocks` (`symbol`, `company`) VALUES(?, ?)', (model.symbol, model.company))
		self.database.commit()

	def find_by_symbol(self, symbol):
		cursor = self.database.execute('SELECT * FROM `stocks` WHERE `symbol` = ? LIMIT 1', (symbol,))
		result = cursor.fetchone()

		return self.build_model(result)

	def build_model(self, data):
		if (data == None):
			return None

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
		self.repository = repository

	def insert(self, model):
		self.repository.insert(model)

class PriceSqliteRepository:
	def __init__(self, database):
		self.database = database

	def insert(self, model):
		self.database.execute('\
			INSERT INTO `prices`\
			(`stock_id`, `year`, `month`, `day`, `closing_price`, `change`)\
			VALUES(?, ?, ?, ?, ?, ?)',
			(model.stock_id, model.year, model.month, model.day, model.closing_price, model.change)
		)
		self.database.commit()
