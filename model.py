from elixir import *

class Location(Entity):
	using_options(inheritance='multi')
	e = Field(Integer)
	n = Field(Integer)

	def __repr__(self):
		return '<Location %sE %sN>' % (self.e, self.n)

class Base(Location):
	using_options(inheritance='multi')
	id = Field(Integer)
	reports = OneToMany('Report')

	def __repr__(self):
		return '<Base %s>' % self.id

class Report(Entity):
	base = ManyToOne('Base')
	team = OneToOne('Team')
	arr = OneToOne('Event')
	dep = OneToOne('Event')

	def __repr__(self):
		return '<Base %s Report: Team %s arr %s dep %s>' % (base.id, team.number, str(arr.time), str(dep.time))

class Event(Entity):
	loc = ManyToOne('Location')
	time = Field(DateTime)

	def __repr__(self):
		return '<Event %s %s>' % (str(self.time), self.loc)

class Team(Entity):
	seen = ManyToMany('Event')
	number = Field(Integer)

	def __repr__(self):
		return '<Team %s>' % self.number
