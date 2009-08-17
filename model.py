from elixir import *
from datetime import datetime, timedelta

class Base(Entity):
	'''The database representation of a manned base'''
	name = Field(Text)
	e = Field(Integer)
	n = Field(Integer)
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
		return cmp(self.name, other.name)

	def ref(self):
		e = str(self.e).rjust(3,'0')
		n = str(self.n).rjust(3,'0')
		return e + n

	def _report(self, filename=None):
		if filename:
			f = open(filename)
		else:
			from sys import stdin
			f = stdin
		for line in f.readlines():
			kwargs = {}
			args = [self]
			for arg in line.split():
				if '=' in arg:
					k,v = arg.split('=')
					kwargs[k] = v
				else:
					args += [arg]
			Report(*args, **kwargs)

	def done(self):
		for route in self.routes:
			for team in route.teams:
				if not team.visited(self):
					return False
		return True

	def active(self, speed=None, maxspeed=None):
		open = None
		close = None
		unknowns = []
		for route in self.routes:
			for team in route.teams:
				slow_eta = team.eta(self, speed)
				if slow_eta:
					if maxspeed:
						fast_eta = team.eta(self, maxspeed)
					else:
						fast_eta = slow_eta
					if open:
						open = min(open, fast_eta)
						close = max(close, slow_eta)
					else:
						open, close = fast_eta, slow_eta
				else:
					unknowns.append(team)
		return {'open':open, 'close':close, 'unknown':unknowns}

	def next(self, route):
		route = Route.get(route)
		if route.end() is self:
			return None
		else:
			n = route.bases.index(self)
			return route.bases[n+1]

	def distance(self, other):
		d = Distance.get_by(start=self, end=other)
		if d:
			return d.distance
		else:
			other = Base.get(other)
			from math import sqrt
			def normalise(diff, rollover=1000):
				diff = abs(diff)
				if diff > rollover//2:
					diff = rollover - diff
				return diff
			ediff = normalise(self.e - other.e)
			ndiff = normalise(self.n - other.n)
			hyp2 = ediff**2 + ndiff**2
			return int(sqrt(hyp2)*self.wfact)

	def distance_along(self, route, other=None):
		route = Route.get(route)
		other = Base.get(other)
		if not other:
			other = self.next(route)
		sum = 0
		start = route.bases.index(self)
		stop = route.bases.index(other)
		for base in route.bases[start:stop]:
			sum += base.distance(base.next(route))
		return sum

	def _set_distance(self, other, d):
		def set(start, end, distance):
			d = Distance.get_by(start=start, end=end)
			if d: d.distance = distance
			else: Distance(start, end, distance)
		set(self, other, d)
		set(other, self, d)

class Route(Entity):
	'''The database representation of a series of bases teams have to pass through'''
	name = Field(Text)
	bases = ManyToMany('Base')
	teams = OneToMany('Team')

	def __init__(self, name, bases=None):
		Entity.__init__(self, name=name)
		if bases:
			for base in bases:
				base = Base.get(base)
				self.bases.append(base)

	def __repr__(self):
		return '<Route %s>' % self.name

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(len(self), len(other))

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
			route = Route.get(route)
			self.route = route

	def __repr__(self):
		return '<Team %s>' % self.name

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.name, other.name)

	def started(self):
		return bool(self.reports)

	def visited(self, base):
		base = Base.get(base)
		for r in self.reports:
			if r.base is base:
				return r.dep
		return False

	def last_visited(self):
		if self.started():
			self.reports.sort(reverse=True)
			return {'base':self.reports[0].base, 'dep':self.reports[0].dep}
		else:
			return {'base':None, 'dep':None}

	def on_route(self):
		if self.route:
			not_started = not self.started()
			last_visited_on_route = self.last_visited()['base'] in self.route.bases
			return not_started or last_visited_on_route
		else:
			return None

	def finished(self):
		if self.route:
			return self.last_visited()['base'] is self.route.end()
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
			return {'walking':walking.seconds // 60, 'stopped':stoppage.seconds // 60}
		else:
			return {'walking':0, 'stopped':0}

	def speed(self):
		t = self.timings()['walking']
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
				last = self.last_visited()['base']
				dep = self.last_visited()['dep']
			else:
				last = self.route.bases[0]
				dep = self.start
			d = last.distance_along(self.route, base)
			if d:
				t = ( d*60 ) // int(speed)
				return dep + timedelta(minutes=t)
			else:
				return None
		else:
			return None

	def late(self, leeway=0, speed=None, base=None):
		eta = self.eta(base, speed)
		if type(leeway).__name__ in ['int', 'str']:
			leeway = timedelta(minutes=int(leeway))
		return eta + leeway < datetime.now()

class Report(Entity):
	'''The database representation of a team's arr/dep times at a base'''
	arr = Field(DateTime)
	dep = Field(DateTime)
	base = ManyToOne('Base')
	team = ManyToOne('Team')

	def __init__(self, base, team, arr, dep=None, date=None):
		base = Base.get(base)
		team = Team.get(team)
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
		return cmp(self.dep, other.dep)

	def stoppage(self):
		return self.dep - self.arr

class Distance(Entity):
	'''Records the distances between two bases'''
	start = ManyToOne('Base')
	end = ManyToOne('Base')
	distance = Field(Integer)

	def __init__(self, start, end, dist=0):
		Entity.__init__(self, distance=int(dist))
		self.start = Base.get(start)
		self.end = Base.get(end)

	def __repr__(self):
		return '<Distance from %s to %s is %d>' % (self.start, self.end, self.distance)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.distance, other.distance)

def _get(cls, name):
	if type(name) == cls: return name
	else: return cls.get_by(name=name)
Entity.get = classmethod(_get)

def mkdt(time, date=None):
	if not date:
		date = START.date()
	elif type(date).__name__ == 'str':
		date = datetime.strptime(date,'%y%m%d').date()
	if type(time).__name__ == 'str':
		time = datetime.strptime(time,'%H:%M').time()
	return datetime.combine(date, time)
START = mkdt('08:00', datetime.today().date())
