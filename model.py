from elixir import *

class Location(Entity):
	e = Field(Integer)
	n = Field(Integer)

	def __repr__(self):
		return '<Location %sE %sN>' % (self.e, self.n)

class Event(Entity):
	loc = ManyToOne('Location')
	time = Field(DateTime)

	def __repr__(self):
		return '<Event %s %s>' % (str(self.time), self.loc)

class Team(Entity):
	seen = ManyToMany('Event')
	number = Field(Integer)

	def __repr__(self):
		return '<Team %s>' % self.number
