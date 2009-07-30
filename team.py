from elixir import *

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
