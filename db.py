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

class route(Named, Entity):
	'''The database representation of a series of bases teams have to pass through'''
	name = Field(Text)

class team(Named, Entity):
	'''The database representation of a competing team'''
	name = Field(Text)
	start = Field(DateTime)

class report(Entity):
	'''The database representation of a team's arr/dep times at a base'''
	arr = Field(DateTime)
	dep = Field(DateTime)
	note = Field(Text)

class leg(Entity):
	'''Records the distance and height gain between two bases'''
	dist = Field(Integer)
	gain = Field(Integer)

class config(Entity):
	'''The hike configuration details'''
	start = Field(DateTime)
	wfact = Field(Float)
	naith = Field(Float)
	figs  = Field(Integer)
	ver   = Field(Text)
