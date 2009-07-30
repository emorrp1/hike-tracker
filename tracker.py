from elixir import *

def start(filename="custom.hike"):
	from os.path import exists
	metadata.bind = "sqlite:///" + filename # connect
	setup_all()
	if not exists(filename):
		create_all()

save = session.commit

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

	def done(self):
		for route in self.routes:
			for team in route.teams:
				if not team.visited(self):
					return False
		return True

	def next(self, route):
		if type(route).__name__ == 'int':
			route = Route.get(route)
		n = route.bases.index(self)
		if len(route.bases) == n+1:
			return None
		else:
			return route.bases[n+1]

	def distance(self, other):
		from math import pow, sqrt
		if type(other).__name__ == 'int':
			other = Base.get(other)
		ediff = self.e - other.e
		ndiff = self.n - other.n
		hyp =  sqrt( pow(ediff, 2) + pow(ndiff, 2))
		return int(hyp)

	def distance_along(self, route, other=None):
		if type(route).__name__ == 'int':
			route = Route.get(route)
		if not other:
			other = self.next(route)
		else:
			if type(other).__name__ == 'int':
				other = Base.get(other)
		sum = 0
		start = route.bases.index(self)
		stop = route.bases.index(other)
		for base in route.bases[start:stop]:
			sum += base.distance(base.next(route))
		return sum

class Route(Entity):
	id = Field(Integer, primary_key=True)
	bases = ManyToMany('Base')
	teams = OneToMany('Team')

	def __init__(self, id, bases=None):
		Entity.__init__(self, id=id)
		if bases:
			for base in bases:
				if type(base).__name__ == 'int':
					base = Base.get(base)
				self.bases.append(base)

	def __repr__(self):
		return '<Route %s>' % self.id

	def __len__(self):
		sum = 0
		for base in self.bases[:-1]:
			sum += base.distance(base.next(self))
		return sum

	def end(self):
		last = len(self.bases) - 1
		return self.bases[last]

class Team(Entity):
	id = Field(Integer, primary_key=True)
	reports = OneToMany('Report')
	route = ManyToOne('Route')

	def __init__(self, id, route=None):
		Entity.__init__(self, id=id)
		if route:
			if type(route).__name__ == 'int':
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

	def last_visited(self):
		self.reports.sort(reverse=True)
		return self.reports[0].base, self.reports[0].dep

	def on_route(self):
		return self.last_visited()[0] in self.route.bases

	def finished(self):
		return self.last_visited()[0] == self.route.end

	def completed(self):
		for base in self.route.bases:
			if not self.visited(base):
				return False
		return True

	def traversed(self):
		sum = 0
		self.reports.sort()
		for i in range(len(self.reports)-1):
			base = self.reports[i].base
			next = self.reports[i+1].base
			sum += base.distance(next)
		return sum

	def timings(self):
		from datetime import timedelta
		walking = timedelta()
		self.reports.sort(reverse=True)
		stoppage = self.reports[0].stoppage()
		self.reports.sort()
		for i in range(len(self.reports)-1):
			r = self.reports[i]
			stoppage += r.stoppage()
			walking += self.reports[i+1].arr - r.dep
		return walking.seconds // 60, stoppage.seconds // 60

	def speed(self):
		d = self.traversed()
		t = self.timings()[0]
		return ( d*60 ) // t

	def eta(self, base=None, sp=None):
		if not self.on_route():
			return None
		from datetime import timedelta
		last, dep = self.last_visited()
		if not sp:
			sp = self.speed()
		d = last.distance_along(self.route, base)
		t = ( d*3600 ) // sp
		return dep + timedelta(0,t)

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

	def stoppage(self):
		return self.dep - self.arr
