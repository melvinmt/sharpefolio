import MySQLdb
import datetime

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

class StockMysqlRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		if model.id == None:
			self._insert_no_pk(model)
		else:
			self._insert_full(model)

	def _insert_full(self, model):
		cursor = self._database.cursor()
		cursor.execute('INSERT INTO `stocks` (`id`, `symbol`, `company`) VALUES(%s, %s, %s)', (model.id, model.symbol, model.company))
		self._database.commit()

	def _insert_no_pk(self, model):
		cursor = self._database.cursor()
		cursor.execute('INSERT INTO `stocks` (`symbol`, `company`) VALUES(%s, %s)', (model.symbol, model.company))
		self._database.commit()

	def find_by_symbol(self, symbol):
		cursor = self._database.cursor()
		cursor._database.execute('SELECT * FROM `stocks` WHERE `symbol` = %s LIMIT 1', (symbol,))
		result = cursor.fetchone()

		return self.build_model(result)

	def find_all(self):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `stocks`')
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

	def loop(self):
		for stock in self._stocks:
			yield self.build_model(stock)

	def build_model(self, data):
		model = Stock(data['symbol'], data['company'])
		model._id = data['id']
		return model;

class Price(object):
	def __init__(self, stock_id, date, closing_price, change):
		self._id = None
		self._stock_id = stock_id
		self._date = date
		self._closing_price = closing_price
		self._change = change

	@property
	def id(self):
		return self._id

	@property
	def stock_id(self):
		return self._stock_id

	@property
	def date(self):
		return self._date

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
		cursor = self._database.cursor()
		cursor.execute("\
			SELECT *, date(year || '-' || substr('00' || month, -2, 2) || '-' || substr('00' || day, -2, 2)) as `date`\
			FROM `prices`\
			WHERE `stock_id` = ? ORDER BY `year` ASC, `month` ASC, `day` ASC", (stock_id,))
		return PriceCollection(cursor)

	def find_by_stock_id_in_range(self, stock_id, start_date, end_date):
		cursor = self._database.execute("\
			SELECT *, date(year || '-' || substr('00' || month, -2, 2) || '-' || substr('00' || day, -2, 2)) as `date`\
			FROM `prices`\
			WHERE `stock_id` = ?\
			AND `date` >= date(?)\
			AND `date` <= date(?)\
			ORDER BY `year` ASC, `month` ASC, `day` ASC", (stock_id, start_date.isoformat(), end_date.isoformat())
		)
		return PriceCollection(cursor)

class PriceMysqlRepository:
	def __init__(self, database):
		self._database = database

	def insert(self, model):
		if model.id == None:
			self._insert_no_pk(model)
		else:
			self._insert_full(model)

	def _insert_full(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `prices`\
			(`id`, `stock_id`, `date`, `closing_price`, `change`)\
			VALUES(%s, %s, %s, %s, %s)',
			(model.id, model.stock_id, model.date, model.closing_price, model.change)
		)
		self._database.commit()

	def _insert_no_pk(self, model):
		cursor = self._database.cursor()
		cursor.execute('\
			INSERT INTO `prices`\
			(`stock_id`, `date`, `closing_price`, `change`)\
			VALUES(%s, %s, %s, %s)',
			(model.stock_id, model.date, model.closing_price, model.change)
		)
		self._database.commit()

	def find_by_stock_id(self, stock_id):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `prices` WHERE `stock_id` = %s ORDER BY `date` ASC', (stock_id,))
		return PriceCollection(cursor)

	def find_by_stock_id_in_range(self, stock_id, start_date, end_date):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("\
			SELECT *\
			FROM `prices`\
			WHERE `stock_id` = %s\
			AND `date` >= %s\
			AND `date` <= %s\
			ORDER BY `date` ASC", (stock_id, start_date.isoformat(), end_date.isoformat())
		)
		return PriceCollection(cursor)

class PriceCollection:
	def __init__(self, prices):
		self._prices = prices

	def loop(self):
		for price in self._prices:
			yield self.build_model(price)

	def build_model(self, data):
		model = Price(
			data['stock_id'],
			datetime.datetime.strptime("%s" % data['date'], "%Y-%m-%d").date(),
			data['closing_price'],
			data['change']
		)
		model._id = data['id']
		return model;
