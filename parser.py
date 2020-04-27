from tensor import Tensor

class Parser:
	
	_operations = {
		'+' : 0,
		'-' : 0,
		'*' : 1,
		'transpose' : -1  
	}

	_max_level = 2

	def __init__(self):
		self._last = None

	def parse(self, s, values):
		self._s = s
		self._pos = 0
		self.values = values
		return self._expression(0)

	def _expect(self, c):
		assert c == self._next()

	def _expect_str(self, s):
		for i in s:
			self._expect(i)

	def _next(self):
		ans = self._cur()
		self._pos += 1
		return ans

	def _cur(self):
		return (self._s[self._pos] if self._pos < len(self._s) else '\0')

	def _test(self, c):
		if c == self._cur():
			self._next()
			return True
		return False

	def _test_str(self, string):
		if self._s[self._pos : self._pos + len(string)] == string:
			self._pos += len(string)
			return True
		return False

	def _test_oper(self):
		for i in Parser._operations.keys():
			if self._test_str(i):
				return i
		return None

	def _skip_ws(self):
		while self._cur().isspace():
			self._next()

	def _simple(self):
		self._skip_ws()
		if self._test('('):
			expr = self._expression(0)
			self._skip_ws()
			self._expect(')')
			return expr
		
		oper = self._test_oper()

		if oper == '-':
			return -self._simple()
		elif oper == 'transpose':
			return self._simple().transpose()

		if self._cur().isdigit():
			return self._number()
		else:
			return self._variable()


	def _number(self):
		self._skip_ws()
		s = ''
		while self._cur().isdigit():
			s += self._next()
		return Tensor(0, 0, 0, int(s))

	def _variable(self):
		s = ''
		self._skip_ws()
		while self._cur().isalpha():
			s += self._next()
		return self.values[s]

	def _expression(self, level):

		if level == Parser._max_level:
			return self._simple()
		else:
			self._skip_ws()
			expr = self._expression(level + 1)
			
			while self._cur() != '\0' or self._last != None:
				if self._last is None:
					self._skip_ws()
					oper = self._test_oper()
				else:
					oper = self._last
					self._last = None

				if oper == None:
					break

				if Parser._operations[oper] != level:
					self._last = oper
					break

				if oper == '+':
					expr = expr + self._expression(level + 1)
				elif oper == '-':
					expr = expr - self._expression(level + 1)
				elif oper == '*':
					expr = expr * self._expression(level + 1)
			return expr



