class Report(object):
	def __init__(self, year, month, day, duration):
		self._id = None
		self._year = year
		self._month = month
		self._day = day;
		self._duration = duration

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
