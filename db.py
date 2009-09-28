from elixir import *

class Named(object):
	'''Modified Entity methods for named objects'''
	def __repr__(self):
		return '<%s %s>' % (self.__class__.__name__, self.name)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.name, other.name)

	@classmethod
	def get(cls, name):
		if isinstance(name, cls) or not name: return name
		else: return cls.get_by(name=name)

class base(Named, Entity):
	'''The database representation of a manned base'''
	name = Field(Text)
	e = Field(Integer)
	n = Field(Integer)
	h = Field(Integer)
