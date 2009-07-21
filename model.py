from elixir import *

class Base(Entity):
	id = Field(Integer)
	e = Field(Integer)
	n = Field(Integer)
	reports = OneToMany('Report')

	def __repr__(self):
		return '<Base %s>' % self.id

class Report(Entity):
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __repr__(self):
		return '<Base %s Report: Team %s arrived %s departed %s>' % (base.id, team.id, str(arr.time()), str(dep.time()))

class Team(Entity):
	id = Field(Integer)
	visited = OneToMany('Report')

	def __repr__(self):
		return '<Team %s>' % self.id
