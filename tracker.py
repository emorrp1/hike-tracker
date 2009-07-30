from elixir import *
from team import *
from base import *

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
