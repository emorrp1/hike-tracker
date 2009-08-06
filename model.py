from elixir import *

class Base(Entity):
	'''The database representation of a manned base'''
	name = Field(Text)
	e = Field(Integer)
	n = Field(Integer)
	reports = OneToMany('Report')
	routes = ManyToMany('Route')

	def __init__(self, name, ref):
		e = int(ref[:3])
		n = int(ref[-3:])
		Entity.__init__(self, name=name, e=e, n=n)

	def __repr__(self):
		return '<Base %s>' % self.name

	def report(self):
		from sys import stdin
		for line in stdin.readlines():
			args = [self] + line.split()
			Report(*args)

	def done(self):
		for route in self.routes:
			for team in route.teams:
				if not team.visited(self):
					return False
		return True

	def next(self, route):
		if type(route).__name__ == 'str':
			route = Route.get_by(name=route)
		n = route.bases.index(self)
		if len(route.bases) == n+1:
			return None
		else:
			return route.bases[n+1]

	def distance(self, other):
		from math import fabs, pow, sqrt
		if type(other).__name__ == 'str':
			other = Base.get_by(name=other)
		rollover = 1000
		ediff = fabs(self.e - other.e)
		if ediff > rollover/2:
			ediff = rollover - ediff
		ndiff = fabs(self.n - other.n)
		if ndiff > rollover/2:
			ndiff = rollover - ndiff
		hyp =  sqrt( pow(ediff, 2) + pow(ndiff, 2))
		return int(hyp)

	def distance_along(self, route, other=None):
		if type(route).__name__ == 'str':
			route = Route.get_by(name=route)
		if not other:
			other = self.next(route)
		else:
			if type(other).__name__ == 'str':
				other = Base.get_by(name=other)
		sum = 0
		start = route.bases.index(self)
		stop = route.bases.index(other)
		for base in route.bases[start:stop]:
			sum += base.distance(base.next(route))
		return sum

class Route(Entity):
	'''The database representation of a series of bases teams have to pass through'''
	name = Field(Text)
	bases = ManyToMany('Base')
	teams = OneToMany('Team')

	def __init__(self, name, bases=None):
		Entity.__init__(self, name=name)
		if bases:
			for base in bases:
				if type(base).__name__ == 'str':
					base = Base.get_by(name=base)
				self.bases.append(base)

	def __repr__(self):
		return '<Route %s>' % self.name

	def __len__(self):
		return self.bases[0].distance_along(self, self.end())

	def end(self):
		last = len(self.bases) - 1
		return self.bases[last]

class Team(Entity):
	'''The database representation of a competing team'''
	name = Field(Text)
	reports = OneToMany('Report')
	route = ManyToOne('Route')

	def __init__(self, name, route=None):
		Entity.__init__(self, name=name)
		if route:
			if type(route).__name__ == 'str':
				route = Route.get_by(name=route)
			self.route = route

	def __repr__(self):
		return '<Team %s>' % self.name

	def __cmp__(self, other):
		if self.name <  other.name: return -1
		if self.name == other.name: return 0
		if self.name >  other.name: return 1

	def visited(self, base):
		if type(base).__name__ == 'str':
			base = Base.get_by(name=base)
		reports = Report.query.filter(Report.team == self)
		return reports.filter(Report.base == base).all()

	def last_visited(self):
		if len(self.reports) == 0:
			return None, None
		self.reports.sort(reverse=True)
		return self.reports[0].base, self.reports[0].dep

	def on_route(self):
		return self.last_visited()[0] in self.route.bases

	def finished(self):
		return self.last_visited()[0] == self.route.end()

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
		if len(self.reports) == 0:
			return 0, 0
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
		if self.finished() or not self.on_route():
			return None
		from datetime import timedelta
		last, dep = self.last_visited()
		if not sp:
			sp = self.speed()
		d = last.distance_along(self.route, base)
		t = ( d*3600 ) // sp
		return dep + timedelta(0,t)

class Report(Entity):
	'''The database representation of a team's arr/dep times at a base'''
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __init__(self, base, team, arr, dep=None, date=None):
		if not dep: dep = arr
		arr = self.mkdt(arr, date)
		dep = self.mkdt(dep, date)
		Entity.__init__(self, arr=arr, dep=dep)
		if type(team).__name__ == 'str':
			team = Team.get_by(name=team)
		self.team = team
		if type(base).__name__ == 'str':
			base = Base.get_by(name=base)
		self.base = base

	def __repr__(self):
		return '<%s Report: %s arrived %s departed %s>' % (self.base, self.team, self.arr.time(), self.dep.time())

	def __cmp__(self, other):
		if self.arr <  other.arr: return -1
		if self.arr == other.arr: return 0
		if self.arr >  other.arr: return 1

	def mkdt(self, time, date=None):
		from datetime import datetime
		if not date: date = datetime.today().strftime('%y%m%d')
		return datetime.strptime(date + time, '%y%m%d%H:%M')

	def stoppage(self):
		return self.dep - self.arr
