from elixir import *

options_defaults['tablename'] = lambda x: x.__name__ + 's'

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
	reports = OneToMany('report')
	routes = ManyToMany('route')

class route(Named, Entity):
	'''The database representation of a series of bases teams have to pass through'''
	name = Field(Text)
	bases = ManyToMany('base')
	teams = OneToMany('team')

class team(Named, Entity):
	'''The database representation of a competing team'''
	name = Field(Text)
	start = Field(DateTime)
	reports = OneToMany('report')
	route = ManyToOne('route')

class report(Entity):
	'''The database representation of a team's arr/dep times at a base'''
	arr = Field(DateTime)
	dep = Field(DateTime)
	note = Field(Text)
	base = ManyToOne('base')
	team = ManyToOne('team')

	def __repr__(self):
		if self.note: NOTE = ' - %s' % self.note
		else: NOTE = ''
		return '<%s Report: %s arrived %s departed %s%s>' % (self.base, self.team, self.arr.time(), self.dep.time(), NOTE)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.dep, other.dep)

class leg(Entity):
	'''Records the distance and height gain between two bases'''
	dist = Field(Integer)
	gain = Field(Integer)
	start = ManyToOne('base')
	end = ManyToOne('base')

	def __repr__(self):
		return '<From %s to %s: distance is %d; height gain is %d>' % (self.start, self.end, self.dist, self.gain)

	def __cmp__(self, other):
		if other is None: return 2
		c = cmp(self.dist, other.dist)
		if c: return c
		else: return cmp(self.gain, other.gain)

class config(Entity):
	'''The hike configuration details'''
	start = Field(DateTime)
	wfact = Field(Float)
	naith = Field(Float)
	figs  = Field(Integer)
	ver   = Field(Text)

	def __repr__(self):
		return '<Global configuration>'
