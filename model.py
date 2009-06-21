from elixir import *

class Location(Entity):
	e = Field(Integer)
	n = Field(Integer)

	def __repr__(self):
		return '<Location %s %s>' % (self.e, self.n)

class Team(Entity):
	number = Field(Integer)

	location = ManyToOne('Location')

	def __repr__(self):
		return '<Team %s>' % self.number
