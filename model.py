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

	def report(self, team, arr, dep=None, date=None):
		Report(self, team, arr, dep, date)

class Route(Entity):
	name = Field(Text, primary_key=True)
	bases = ManyToMany('Base')
	teams = OneToMany('Team')

	def __init__(self, name, bases=None):
		Entity.__init__(self, name=name)
		if bases:
			for base in bases:
				if type(base).__name__ == 'int':
					base = Base.get(base)
				self.bases.append(base)

	def __repr__(self):
		return '<Route %s>' % self.name

class Team(Entity):
	id = Field(Integer, primary_key=True)
	reports = OneToMany('Report')
	route = ManyToOne('Route')

	def __init__(self, id, route=None):
		Entity.__init__(self, id=id)
		if route:
			if type(route).__name__ == 'str':
				route = Route.get(route)
			self.route = route

	def __repr__(self):
		return '<Team %s>' % self.id

	def __cmp__(self, other):
		if self.id <  other.id: return -1
		if self.id == other.id: return 0
		if self.id >  other.id: return 1

	def visited(self, base):
		if type(base).__name__ == 'int':
			base = Base.get(base)
		reports = Report.query.filter(Report.team == self)
		return reports.filter(Report.base == base).all()

	def completed(self):
		for base in self.route.bases:
			if not self.visited(base):
				return False
		return True

class Report(Entity):
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __init__(self, base, team, arr, dep=None, date=None):
		if not dep: dep = arr
		arr = mkdt(arr, date)
		dep = mkdt(dep, date)
		Entity.__init__(self, arr=arr, dep=dep)
		if type(team).__name__ == 'int':
			team = Team.get(team)
		self.team = team
		if type(base).__name__ == 'int':
			base = Base.get(base)
		self.base = base

	def __repr__(self):
		return '<%s Report: %s arrived %s departed %s>' % (self.base, self.team, self.arr.time(), self.dep.time())

	def __cmp__(self, other):
		if self.arr <  other.arr: return -1
		if self.arr == other.arr: return 0
		if self.arr >  other.arr: return 1
