from elixir import *
from datetime import datetime
DATE='090721'

class Base(Entity):
	id = Field(Integer)
	e = Field(Integer)
	n = Field(Integer)
	reports = OneToMany('Report')

	def report(self, team_id, arr, dep, date=DATE)
		arr = datetime(int(date[:2]),int(date[2:-2]),int(date[-2:]),int(arr[:2]),int(arr[-2:]))
		dep = datetime(int(date[:2]),int(date[2:-2]),int(date[-2:]),int(dep[:2]),int(dep[-2:]))
		team = Team.get_by(id=team_id)
		reports.append(Report(arr=

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
