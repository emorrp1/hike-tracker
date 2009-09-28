from elixir import *
from datetime import datetime, timedelta
import db
from db import Named

__version__ = db.VERSION

class Base(db.base):
	def __init__(self, name, ref, height=0):
		f = conf().figs//2
		e = int(ref[:f])
		n = int(ref[-f:])
		Entity.__init__(self, name=name, e=e, n=n, h=int(height))

	def ref(self):
		f = conf().figs//2
		e = str(self.e).rjust(f,'0')
		n = str(self.n).rjust(f,'0')
		return e + n

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
		return route.next(self)

	def distance(self, other):
		return Leg.get(self, other).dist

	def gain(self, other):
		return Leg.get(self, other).gain

	def distgain_along(self, route, other=None):
		route = Route.get(route)
		return route.distgain_from(self, other)

	def _set_distance(self, other, d):
		Leg.set(self, other, d)

class Route(db.route):
	def __init__(self, name, bases=None):
		Entity.__init__(self, name=name)
		if bases:
			for base in bases:
				base = Base.get(base)
				self.bases.append(base)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(len(self), len(other))

	def __len__(self):
		return self.distgain_from(self.bases[0], self.end())['dist']

	def next(self, base):
		base = Base.get(base)
		if base is self.end():
			return None
		else:
			n = self.bases.index(base)
			return self.bases[n+1]

	def end(self):
		last = len(self.bases) - 1
		return self.bases[last]

	def legs(self, start=None, end=None):
		b = self.bases
		if start: start = b.index(Base.get(start))
		else:     start = 0
		if end: end = b.index(Base.get(end))
		else: end = len(b) - 1
		legs = []
		for i in range(start, end):
			l = Leg.get(b[i],b[i+1])
			legs += [l]
		return legs

	def distgain_from(self, base, other=None):
		base = Base.get(base)
		other = Base.get(other)
		if not other:
			other = base.next(self)
		dist = 0
		gain = 0
		for l in self.legs(base, other):
			dist += l.dist
			gain += l.gain
		return {'dist':dist, 'gain':gain}

class Team(db.team):
	def __init__(self, name, route=None, start=None):
		if start: start = mkdt(start)
		else:     start = conf().start
		Entity.__init__(self, name=name, start=start)
		if route: self.route = Route.get(route)

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

	def missed(self):
		if self.route and self.finished():
			count = 0
			for base in self.route.bases:
				if not self.visited(base):
					count += 1
			return count
		else:
			return -1

	def traversed(self):
		dist = 0
		gain = 0
		self.reports.sort()
		for i in range(len(self.reports)-1):
			base = self.reports[i].base
			next = self.reports[i+1].base
			l = Leg.get(base, next)
			dist += l.dist
			gain += l.gain
		return {'dist':dist, 'gain':gain}

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
			tr = self.traversed()
			t -= tr['gain']*conf().naith
			return ( tr['dist']*60 ) // t
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
			dg = self.route.distgain_from(last, base)
			if dg['dist']:
				t = ( dg['dist']*60 ) // int(speed)
				t += dg['gain']*conf().naith
				return dep + timedelta(minutes=t)
			else:
				return None
		else:
			return None

	def late(self, leeway=0, speed=None, base=None):
		eta = self.eta(base, speed)
		if eta:
			if isinstance(leeway, (int, str, unicode)):
				leeway = timedelta(minutes=int(leeway))
			return eta + leeway < datetime.now()
		else:
			return None

class Report(db.report):
	def __init__(self, base, team, arr, dep=None, date=None, note=None):
		arr = mkdt(arr, date)
		if dep: dep = mkdt(dep, date)
		else: dep = arr
		Entity.__init__(self, arr=arr, dep=dep, note=note)
		self.base = Base.get(base)
		self.team = Team.get(team)

	def __repr__(self):
		if self.note: NOTE = ' - %s' % self.note
		else: NOTE = ''
		return '<%s Report: %s arrived %s departed %s%s>' % (self.base, self.team, self.arr.time(), self.dep.time(), NOTE)

	def __cmp__(self, other):
		if other is None: return 2
		return cmp(self.dep, other.dep)

	def stoppage(self):
		return self.dep - self.arr

class Leg(db.leg):
	def __init__(self, start, end, dist=None, gain=None):
		Entity.__init__(self)
		self.start = Base.get(start)
		self.end = Base.get(end)
		if dist: self.dist = int(dist)
		else:    self.dist = self._calc_dist()
		if gain: self.gain = int(gain)
		else:    self.gain = self._calc_gain()

	def __repr__(self):
		return '<From %s to %s: distance is %d; height gain is %d>' % (self.start, self.end, self.dist, self.gain)

	def __cmp__(self, other):
		if other is None: return 2
		c = cmp(self.dist, other.dist)
		if c: return c
		else: return cmp(self.gain, other.gain)

	def _calc_dist(self):
		from math import sqrt
		def normalise(diff, rollover=None):
			if not rollover: rollover=10**(conf().figs//2)
			diff = abs(diff)
			if diff > rollover//2:
				diff = rollover - diff
			return diff
		ediff = normalise(self.start.e - self.end.e)
		ndiff = normalise(self.start.n - self.end.n)
		hyp2 = ediff**2 + ndiff**2
		return int(sqrt(hyp2)*conf().wfact)

	def _calc_gain(self):
		diff = self.end.h - self.start.h
		if diff < 0: diff = 0
		return diff//10 # no. of contours

	@classmethod
	def get(cls, start, end):
		start = Base.get(start)
		end = Base.get(end)
		l = cls.get_by(start=start, end=end)
		if not l: l = cls(start, end)
		return l

	@classmethod
	def _set(cls, start, end, dist=None, gain=None):
		d = cls.get(start, end)
		if dist is not None:
			if dist: d.dist = int(dist)
			else:    d.dist = d._calc_dist()
		if gain is not None:
			if gain: d.gain = int(gain)
			else:    d.gain = d._calc_dist()

	@classmethod
	def set(cls, start, end, dist=None, gain=None):
		cls._set(start, end, dist, gain)
		cls._set(end, start, dist)

class Config(db.config):
	def __repr__(self):
		return '<Global configuration>'

def conf():
	c = Config.query.first()
	if c:
		return c
	else:
		defaults = {
				'start': mkdt('08:00', datetime.today().date()),
				'wfact': 1.3,
				'naith': 1.0,
				'figs' : 6,
				'ver'  : __version__ }
		return Config(**defaults)

def mkdt(time, date=None):
	if not date:
		date = conf().start.date()
	elif isinstance(date, (str, unicode)):
		date = datetime.strptime(date,'%y%m%d').date()
	if isinstance(time, (str, unicode)):
		time = datetime.strptime(time,'%H:%M').time()
	return datetime.combine(date, time)
