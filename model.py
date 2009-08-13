from elixir import *
from datetime import datetime, timedelta

class Base(Entity):
	'''The database representation of a manned base'''
	name = Field(Text)
	e = Field(Integer)
	n = Field(Integer)
	distances = {}
	wfact = 1.3
	reports = OneToMany('Report')
	routes = ManyToMany('Route')

	def __init__(self, name, ref):
		e = int(ref[:3])
		n = int(ref[-3:])
		Entity.__init__(self, name=name, e=e, n=n)

	def __repr__(self):
		return '<Base %s>' % self.name

	def __cmp__(self, other):
		if other is None: return 2
		if self.name <  other.name: return -1
		if self.name == other.name: return 0
		if self.name >  other.name: return 1

	def report(self, filename=None):
		if filename:
			f = open(filename)
		else:
			from sys import stdin
			f = stdin
		for line in f.readlines():
			args = [self] + line.split()
			Report(*args)

	def done(self):
		for route in self.routes:
			for team in route.teams:
				if not team.visited(self):
					return False
		return True

	def active(self, speed=None):
		open = None
		close = None
		unknowns = []
		for route in self.routes:
			for team in route.teams:
				eta = team.eta(self, speed)
				if eta:
					if open:
						open = min(open, eta)
						close = max(close, eta)
					else:
						open, close = eta, eta
				else:
					unknowns.append(team)
		return {'open':open, 'close':close, 'unknown':unknowns}

	def next(self, route):
		if type(route).__name__ == 'str':
			route = Route.get_by(name=route)
		if route.end() is self:
			return None
		else:
			n = route.bases.index(self)
			return route.bases[n+1]

	def distance(self, other):
		if type(other).__name__ == 'str':
			other = Base.get_by(name=other)
		if self.distances:
			try:    return self.distances[self.name][other.name]
			except: pass
		from math import sqrt
		def normalise(diff, rollover=1000):
			diff = abs(diff)
			if diff > rollover//2:
				diff = rollover - diff
			return diff
		ediff = normalise(self.e - other.e)
		ndiff = normalise(self.n - other.n)
		hyp2 = pow(ediff, 2) + pow(ndiff, 2)
		return int(sqrt(hyp2)*self.wfact)

	def distance_along(self, route, other=None):
		if type(route).__name__ == 'str':
			route = Route.get_by(name=route)
		if type(other).__name__ == 'str':
			other = Base.get_by(name=other)
		if not other:
			other = self.next(route)
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

	def __cmp__(self, other):
		if other is None: return 2
		if len(self) <  len(other): return -1
		if len(self) == len(other): return 0
		if len(self) >  len(other): return 1

	def __len__(self):
		return self.bases[0].distance_along(self, self.end())

	def end(self):
		last = len(self.bases) - 1
		return self.bases[last]

class Team(Entity):
	'''The database representation of a competing team'''
	name = Field(Text)
	start = Field(DateTime)
	reports = OneToMany('Report')
	route = ManyToOne('Route')

	def __init__(self, name, route=None, start=None):
		Entity.__init__(self, name=name)
		if start:
			self.start = mkdt(start)
		else:
			self.start = START
		if route:
			if type(route).__name__ == 'str':
				route = Route.get_by(name=route)
			self.route = route

	def __repr__(self):
		return '<Team %s>' % self.name

	def __cmp__(self, other):
		if other is None: return 2
		if self.name <  other.name: return -1
		if self.name == other.name: return 0
		if self.name >  other.name: return 1

	def started(self):
		return bool(self.reports)

	def visited(self, base):
		if type(base).__name__ == 'str':
			base = Base.get_by(name=base)
		for r in self.reports:
			if r.base is base:
				return r.dep
		return False

	def last_visited(self):
		if self.started():
			self.reports.sort(reverse=True)
			return self.reports[0].base, self.reports[0].dep
		else:
			return None, None

	def on_route(self):
		if self.route:
			not_started = not self.started()
			last_visited_on_route = self.last_visited()[0] in self.route.bases
			return not_started or last_visited_on_route
		else:
			return None

	def finished(self):
		if self.route:
			return self.last_visited()[0] is self.route.end()
		else:
			return None

	def completed(self):
		if self.route:
			for base in self.route.bases:
				if not self.visited(base):
					return False
			return True
		return None

	def traversed(self):
		sum = 0
		self.reports.sort()
		for i in range(len(self.reports)-1):
			base = self.reports[i].base
			next = self.reports[i+1].base
			sum += base.distance(next)
		return sum

	def timings(self):
		if self.started():
			walking = timedelta()
			self.reports.sort(reverse=True)
			stoppage = self.reports[0].stoppage()
			self.reports.sort()
			for i in range(len(self.reports)-1):
				r = self.reports[i]
				stoppage += r.stoppage()
				walking += self.reports[i+1].arr - r.dep
			return walking.seconds // 60, stoppage.seconds // 60
		else:
			return 0, 0

	def speed(self):
		t = self.timings()[0]
		if t:
			d = self.traversed()
			return ( d*60 ) // t
		else:
			return None

	def eta(self, base=None, speed=None):
		if base:
			t = self.visited(base)
			if t:
				return t
		if not speed:
			speed = self.speed()
		if not self.finished() and self.on_route() and speed:
			if self.started():
				last, dep = self.last_visited()
			else:
				last = self.route.bases[0]
				dep = self.start
			d = last.distance_along(self.route, base)
			if d:
				t = ( d*3600 ) // speed
				return dep + timedelta(0,t)
			else:
				return None
		else:
			return None

class Report(Entity):
	'''The database representation of a team's arr/dep times at a base'''
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __init__(self, base, team, arr, dep=None, date=None):
		if type(base).__name__ == 'str':
			base = Base.get_by(name=base)
		if type(team).__name__ == 'str':
			team = Team.get_by(name=team)
		arr = mkdt(arr, date)
		if dep:
			dep = mkdt(dep, date)
		else:
			dep = arr
		Entity.__init__(self, arr=arr, dep=dep)
		self.team = team
		self.base = base

	def __repr__(self):
		return '<%s Report: %s arrived %s departed %s>' % (self.base, self.team, self.arr.time(), self.dep.time())

	def __cmp__(self, other):
		if other is None: return 2
		if self.dep <  other.dep: return -1
		if self.dep == other.dep: return 0
		if self.dep >  other.dep: return 1

	def stoppage(self):
		return self.dep - self.arr

START = datetime.today()
def mkdt(time, date=None):
	if not date:
		date = START.strftime('%y%m%d')
	return datetime.strptime(date + time, '%y%m%d%H:%M')
