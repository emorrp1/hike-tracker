from elixir import *

class Location(Entity):
  using_options(inheritance='multi')
  e = Field(Integer)
  n = Field(Integer)
  t = Field(Integer) #minutes since set time

  def __repr__(self):
    return '<Location %s %s>' % (self.x-coord, self.y-coord)

class Team(Entity):
  number = Field(Integer)

  location = ManyToOne('Location')

  def __repr__(self):
    return '<Team %s>' % self.id
