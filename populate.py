#!/usr/bin/python
from elixir import *
from model import *
from datetime import datetime

metadata.bind = "sqlite:///custom.hike" # connect

setup_all()

b0 = Base(id=0,e=0,n=0)
b1 = Base(id=1,e=10,n=0)
b2 = Base(id=2,e=10,n=10)
b3 = Base(id=3,e=0,n=10)

t1 = Team(number=101)
t2 = Team(number=102)
t3 = Team(number=103)
t4 = Team(number=104)

session.commit()

b0.report(101, '12:00')
b0.report(102, '12:00')
b0.report(103, '12:00')
b0.report(104, '12:00')

b1.report(101, '12:15')
b1.report(102, '12:45')
b1.report(103, '12:45')
b1.report(104, '12:45')

b2.report(102, '12:30')
b2.report(103, '12:15')
b2.report(104, '12:15', '12:30')

b3.report(101, '12:45')
b3.report(102, '12:15')
b3.report(103, '12:30')

session.commit()
