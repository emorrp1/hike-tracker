#!/usr/bin/python -W ignore::DeprecationWarning
from tracker import *
from os import path

if not path.exists("custom.hike"):
	execfile("populate.py")

start()

b0 = Base.get(0)
b1 = Base.get(1)
b2 = Base.get(2)
b3 = Base.get(3)

r1 = Route.get(1)
r2 = Route.get(2)

t1 = Team.get(1)
t2 = Team.get(2)
t3 = Team.get(3)
t4 = Team.get(4)

assert b0.done() is True
assert b1.done() is False
assert b2.done() is True
assert b3.done() is False

assert b0.next(r1) is b1
assert b1.next(1) is b3
assert b3.next(r1) is b2
assert b2.next(1) is None
assert b0.next(r2) is b2
assert b2.next(2) is b3
assert b3.next(r2) is None

assert t1.completed() is False
assert t2.completed() is True
assert t3.completed() is True
assert t4.completed() is False

assert t1.visited(3) == []
Report(b3, t1, '13:00')
assert t1.completed() is True
assert b3.done() is True

assert t4.visited(b1) == []
Report(b1, 4, '13:00')
assert t4.completed() is True
assert b1.done() is True
