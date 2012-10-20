from sqlalchemy import *
from sqlalchemy.orm import mapper, relationship, scoped_session, sessionmaker
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declarative_base, declared_attr, has_inherited_table
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.ext.orderinglist import ordering_list
from functools import total_ordering

Session = scoped_session(sessionmaker())
session = Session()

@listens_for(mapper, 'init')
def auto_add(target, args, kwargs):
    Session.add(target)

class BaseClass:
	id = Column(Integer, primary_key=True)
	query = Session.query_property()
	row_type = Column(String(50))

	__table_args__ = {'keep_existing':True}

	@declared_attr
	def __mapper_args__(cls):
		if has_inherited_table(cls):
			return {'polymorphic_identity': cls.__name__.lower()}
		return {'polymorphic_on': cls.row_type}

	@declared_attr
	def __tablename__(cls):
		if has_inherited_table(cls):
			return None
		return cls.__name__.lower() + 's'

Entity = declarative_base(cls=BaseClass)

@total_ordering
class Named:
	'''Modified BaseClass methods for named objects'''
	name = Column(Text)
	query = Session.query_property()

	def __repr__(self):
		return '<%s %s>' % (self.__class__.__name__, self.name)

	def __lt__(self, other):
		if other is None: return False
		return self.name < other.name

	def __eq__(self, other):
		if other is None: return False
		if self.__class__ != other.__class__: return NotImplemented
		return self.name == other.name

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
		collection_class=ordering_list('position'))
	bases = AssociationProxy('base_refs', 'base')
	teams = relationship('team', backref='route')

class routes_bases_order(Entity):
	'''The reference entity for ordered list of bases in route'''
	id = None
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

@total_ordering
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

	def __lt__(self, other):
		if other is None: return False
		return self.dep < other.dep

	def __eq__(self, other):
		if other is None: return False
		if self.__class__ != other.__class__: return NotImplemented
		return self.dep == other.dep

@total_ordering
class leg(Entity):
	'''Records the distance and height gain between two bases'''
	dist = Column(Integer)
	gain = Column(Integer)
	start_id = Column(Integer, ForeignKey(base.id))
	start = relationship('base', primaryjoin='base.id==leg.start_id')
	end_id = Column(Integer, ForeignKey(base.id))
	end = relationship('base', primaryjoin='base.id==leg.end_id')

	def __repr__(self):
		return '<From %s to %s: distance is %d; height gain is %d>' % (self.start, self.end, self.dist, self.gain)

	def __lt__(self, other):
		if other is None: return False
		if self.dist == other.dist: return self.gain < other.gain
		else: return self.dist < other.dist

	def __eq__(self, other):
		if other is None: return False
		if self.__class__ != other.__class__: return NotImplemented
		return self.dist == other.dist and self.gain == other.gain

class config(Entity):
	'''The hike configuration details'''
	start = Column(DateTime)
	wfact = Column(Float)
	naith = Column(Float)
	figs  = Column(Integer)
	ver   = Column(Text)

	def __repr__(self):
		return '<Global configuration>'
