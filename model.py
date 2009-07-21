from elixir import *

DATE='090721'
def mkdt(time, date=DATE):
	from datetime import datetime
	y = int(date[:2])
	m = int(date[2:-2])
	d = int(date[-2:])
	hh = int(time[:2])
	mm = int(time[-2:])
	return datetime(y, m, d, hh, mm)

class Base(Entity):
	id = Field(Integer)
	e = Field(Integer)
	n = Field(Integer)
	reports = OneToMany('Report')

	def report(self, team_id, arr, dep, date=DATE)
		arr = mkdt(arr, date)
		dep = mkdt(arr, date)
		r = Report(arr=arr, dep=dep)
		r.team = Team.get_by(id=team_id)
		self.reports.append(r)

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
