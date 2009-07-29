from elixir import *

DATE='090721'
def mkdt(time, date=DATE):
	from datetime import datetime
	y = int(date[:2])
	m = date[2:-2]
	if len(m) == 4: m = m[1:-1]
	m = int(m)
	d = int(date[-2:])
	hh = int(time[:2])
	mm = int(time[-2:])
	return datetime(y, m, d, hh, mm)

class Base(Entity):
	id = Field(Integer, primary_key=True)
	e = Field(Integer)
	n = Field(Integer)
	reports = OneToMany('Report')

	def __init__(self, id, ref):
		e = int(ref[:3])
		n = int(ref[-3:])
		Entity.__init__(self, id=id, e=e, n=n)

	def __repr__(self):
		return '<Base %s>' % self.id

class Report(Entity):
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __init__(self, base_id, team_id, arr, dep=None, date=DATE):
		if not dep: dep = arr
		arr = mkdt(arr, date)
		dep = mkdt(dep, date)
		Entity.__init__(self, arr=arr, dep=dep)
		self.team = Team.get_by(id=team_id)
		self.base = Base.get_by(id=base_id)

	def __repr__(self):
		return '<Base %s Report: Team %s arrived %s departed %s>' % (base.id, team.id, str(arr.time()), str(dep.time()))

class Team(Entity):
	id = Field(Integer, primary_key=True)
	visited = OneToMany('Report')

	def __init__(self, id):
		Entity.__init__(self, id=id)

	def __repr__(self):
		return '<Team %s>' % self.id
