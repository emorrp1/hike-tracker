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
	team = ManyToOne('Team')
	arr = Field(DateTime)
	dep = Field(DateTime)

	def __repr__(self):
		return '<Base %s Report: Team %s arr %s dep %s>' % (base.id, team.number, str(arr), str(dep))

class Team(Entity):
	visited = OneToMany('Report')
	number = Field(Integer)

	def __repr__(self):
		return '<Team %s>' % self.number
