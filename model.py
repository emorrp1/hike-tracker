from elixir import *

class Location(Entity):
	e = Field(Integer)
	n = Field(Integer)

	def __repr__(self):
		return '<Location %s %s>' % (self.e, self.n)

class Event(Entity):
	loc = ManyToOne('Location')
	time = Field(DateTime)

	def __repr__(self):
		return '<Event %s %sE %sN>' % (str(self.time), self.loc.e, self.loc.n)

class Team(Entity):
	number = Field(Integer)

	location = ManyToOne('Location')

	def __repr__(self):
		return '<Team %s>' % self.number
