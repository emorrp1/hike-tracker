from sqlalchemy import *
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.ext.orderinglist import ordering_list

Session = scoped_session(sessionmaker())

class BaseClass:
	id = Column(Integer, primary_key=True)
	query = Session.query_property()

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower() + 's'

Entity = declarative_base(cls=BaseClass)

class Named:
	'''Modified BaseClass methods for named objects'''
	name = Column(Text)
	query = Session.query_property()

	def __repr__(self):
		return '<%s %s>' % (self.__class__.__name__, self.name)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.name, other.name)

	@classmethod
	def get(cls, name):
		if isinstance(name, cls) or not name: return name
		else: return cls.query.filter_by(name=name).first()

class base(Named, Entity):
	'''The database representation of a manned base'''
	e = Column(Integer)
	n = Column(Integer)
	h = Column(Integer)
	reports = relationship('report', backref='base')
	route_refs = relationship('routes_bases_order', backref='base')
	routes = AssociationProxy('route_refs', 'route')

class route(Named, Entity):
	'''The database representation of a series of bases teams have to pass through'''
	base_refs = relationship('routes_bases_order', backref='route',
		order_by='position',
		collection_class=ordering_list('position'))
	bases = AssociationProxy('base_refs', 'base')
	teams = relationship('team', backref='route')

class routes_bases_order(Entity):
	'''The reference entity for ordered list of bases in route'''
	def __init__(self, arg):
		if isinstance(arg, route): self.route = arg
		if isinstance(arg, base): self.base = arg
	route_id = Column(Integer, ForeignKey(route.id), primary_key=True)
	base_id = Column(Integer, ForeignKey(base.id), primary_key=True)
	position = Column(Integer)

class team(Named, Entity):
	'''The database representation of a competing team'''
	start = Column(DateTime)
	route_id = Column(Integer, ForeignKey(route.id))
	reports = relationship('report', backref='team')

class report(Entity):
	'''The database representation of a team's arr/dep times at a base'''
	arr = Column(DateTime)
	dep = Column(DateTime)
	note = Column(Text)
	base_id = Column(Integer, ForeignKey(base.id))
	team_id = Column(Integer, ForeignKey(team.id))

	def __repr__(self):
		if self.note: NOTE = ' - %s' % self.note
		else: NOTE = ''
		return '<%s Report: %s arrived %s departed %s%s>' % (self.base, self.team, self.arr.time(), self.dep.time(), NOTE)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.dep, other.dep)

class leg(Entity):
	'''Records the distance and height gain between two bases'''
	dist = Column(Integer)
	gain = Column(Integer)
	start_id = Column(Integer, ForeignKey(base.id))
	start = relationship('base')
	end_id = Column(Integer, ForeignKey(base.id))
	start = relationship('base')

	def __repr__(self):
		return '<From %s to %s: distance is %d; height gain is %d>' % (self.start, self.end, self.dist, self.gain)

	def __cmp__(self, other):
		if other is None: return 2
		c = cmp(self.dist, other.dist)
		if c: return c
		else: return cmp(self.gain, other.gain)

class config(Entity):
	'''The hike configuration details'''
	start = Column(DateTime)
	wfact = Column(Float)
	naith = Column(Float)
	figs  = Column(Integer)
	ver   = Column(Text)

	def __repr__(self):
		return '<Global configuration>'
