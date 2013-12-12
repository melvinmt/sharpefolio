import MySQLdb
import datetime
import datamapper as dm

class Stock(object):
	def __init__(self, symbol, company, id = None):
		self.id = id
		self.symbol = symbol
		self.company = company

class StockMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

	def find_by_symbol(self, symbol):
		return self._repository.find_by_symbol(symbol)

	def find_by_id(self, id):
		return self._repository.find_by_id(id)

	def find_all(self):
		return self._repository.find_all()

class StockSqliteRepository(dm.SqliteRepository):
	def insert(self, model):
		self._database.execute('INSERT INTO `stocks` (`symbol`, `company`) VALUES(?, ?)', (model.symbol, model.company))
		self._database.commit()

	def find_by_symbol(self, symbol):
		cursor = self._database.execute('SELECT * FROM `stocks` WHERE `symbol` = ? LIMIT 1', (symbol,))
		result = cursor.fetchone()
		return Stock(**result)

	def find_by_id(self, id):
		cursor = self._database.execute('SELECT * FROM `stocks` WHERE `id` = ? LIMIT 1', (id,))
		result = cursor.fetchone()
		return Stock(**result)

	def find_all(self):
		cursor = self._database.execute('SELECT * FROM `stocks`')
		return dm.Collection(Stock, cursor)

class StockMysqlRepository(dm.MysqlRepository):
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
		cursor.execute('SELECT * FROM `stocks` WHERE `symbol` = %s LIMIT 1', (symbol,))
		result = cursor.fetchone()
		return Stock(**result)

	def find_by_id(self, id):
		cursor = self._database.cursor()
		cursor.execute('SELECT * FROM `stocks` WHERE `id` = %s LIMIT 1', (id,))
		result = cursor.fetchone()
		return Stock(**result)

	def find_all(self):
		cursor = self._database.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM `stocks`')
		return dm.Collection(Stock, cursor)

class Price(object):
	def __init__(self, stock_id, date, closing_price, change, id = None):
		self.id = id
		self.stock_id = stock_id
		self.date = date
		self.closing_price = closing_price
		self.change = change

class PriceMapper(dm.Mapper):
	def insert(self, model):
		self._repository.insert(model)

	def find_by_stock_id(self, stock_id):
		return self._repository.find_by_stock_id(stock_id)

	def find_by_stock_id_in_range(self, stock_id, start_date, end_date):
		return self._repository.find_by_stock_id_in_range(stock_id, start_date, end_date)

class PriceSqliteRepository(dm.SqliteRepository):
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
		return dm.Collection(Price, cursor, self._datamap)

	def find_by_stock_id_in_range(self, stock_id, start_date, end_date):
		cursor = self._database.execute("\
			SELECT *, date(year || '-' || substr('00' || month, -2, 2) || '-' || substr('00' || day, -2, 2)) as `date`\
			FROM `prices`\
			WHERE `stock_id` = ?\
			AND `date` >= date(?)\
			AND `date` <= date(?)\
			ORDER BY `year` ASC, `month` ASC, `day` ASC", (stock_id, start_date.isoformat(), end_date.isoformat())
		)
		return dm.Collection(Price, cursor, self._datamap)

	def _datamap(self, data):
		data['date'] = datetime.datetime.strptime("%s" % data['date'], "%Y-%m-%d").date()
		return data

class PriceMysqlRepository(dm.MysqlRepository):
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
		return dm.Collection(Price, cursor)

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
		return dm.Collection(Price, cursor)
