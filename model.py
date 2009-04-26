from elixir import *

class Location(Entity):
  using_options(inheritance='multi')
  e = Field(Integer)
  n = Field(Integer)
  t = Field(Integer) #minutes since set time

  def __repr__(self):
    return '<Location %s %s>' % (self.x-coord, self.y-coord)

class Base(Location):
  using_options(inheritance='multi')
  name = Field(Unicode(5))

  stewards = OneToMany('Steward')
  routes = ManyToMany('Route')

  def __repr__(self):
    return '<Base "%s">' % self.name

class Person(Entity):
  using_options(inheritance='multi')
  name = Field(Unicode(60))

  def __repr__(self):
    return '<Person "%s">' % self.name

class Steward(Person):
  using_options(inheritance='multi')
  role = Field(Unicode(20))

  base = ManyToOne('Base')

  def __repr__(self):
    return '<Steward "%s">' % self.name

class Participant(Person):
  using_options(inheritance='multi')

  team = ManyToOne('Team')

  def __repr__(self):
    return '<Participant "%s">' % self.name

class Team(Entity):
  number = Field(Integer)

  participants = OneToMany('Participant')
  location = ManyToOne('Location')
  route = ManyToOne('Route')

  def __repr__(self):
    return '<Team %s>' % self.id

class Route(Entity):
  section = Field(Unicode(5))
  bases = ManyToMany('Base')
  teams = OneToMany('Team')

  def __repr__(self):
    return '<Route %s>' % self.section
