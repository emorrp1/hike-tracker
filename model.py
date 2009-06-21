from elixir import *

class Location(Entity):
  e = Field(Integer)
  n = Field(Integer)

  def __repr__(self):
    return '<Location %s %s>' % (self.x-coord, self.y-coord)

class Team(Entity):
  number = Field(Integer)

  location = ManyToOne('Location')

  def __repr__(self):
    return '<Team %s>' % self.id
