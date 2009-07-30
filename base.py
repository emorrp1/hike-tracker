from elixir import *

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
		from math import fabs, pow, sqrt
		if type(other).__name__ == 'int':
			other = Base.get(other)
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
