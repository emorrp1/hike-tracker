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
		return '<Base %s Report: Team %s arrived %s departed %s>' % (base.id, team.number, str(arr), str(dep))

class Team(Entity):
	visited = OneToMany('Report')
	number = Field(Integer)

	def __repr__(self):
		return '<Team %s>' % self.number
