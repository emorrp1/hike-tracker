from elixir import *

def mkdt(time, date=None):
	from datetime import datetime
	if not date: date = datetime.today().strftime('%y%m%d')
	return datetime.strptime(date + time, '%y%m%d%H:%M')

class Base(Entity):
	id = Field(Integer, primary_key=True)
	e = Field(Integer)
	n = Field(Integer)
	reports = OneToMany('Report')
	routes = ManyToMany('Route')

	def __init__(self, id, ref):
		e = int(ref[:3])
		n = int(ref[-3:])
		Entity.__init__(self, id=id, e=e, n=n)

	def __repr__(self):
		return '<Base %s>' % self.id

	def report(self, team_id, arr, dep=None, date=None):
		Report(self.id, team_id, arr, dep, date)

class Report(Entity):
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __init__(self, base_id, team_id, arr, dep=None, date=None):
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
	route = ManyToOne('Route')

	def __init__(self, id, route=None):
		Entity.__init__(self, id=id)
		if route: self.route = Route.get_by(name=route)

	def __repr__(self):
		return '<Team %s>' % self.id

class Route(Entity):
	name = Field(UnicodeText, primary_key=True)
	bases = ManyToMany('Base')
	teams = OneToMany('Team')

	def __init__(self, name, bases=None, teams=None):
		Entity.__init__(self, name=name)
		if bases: for base_id in bases:
			self.bases.append(Base.get_by(id=base_id))
		if teams: for team_id in teams:
			self.teams.append(Team.get_by(id=team_id))

	def __repr__(self):
		return '<Route %s>' % self.name
