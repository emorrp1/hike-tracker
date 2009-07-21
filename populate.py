#!/usr/bin/python
from elixir import *
from model import *
from datetime import datetime

metadata.bind = "sqlite:///custom.hike" # connect

setup_all()

b00 = Base(id=0,e=0,n=0)
b10 = Base(id=1,e=10,n=0)
b11 = Base(id=2,e=10,n=10)
b01 = Base(id=3,e=0,n=10)

t1 = Team(number=101)
t2 = Team(number=102)
t3 = Team(number=103)
t4 = Team(number=104)

session.commit()

b00.report(101, '12:00')
b00.report(102, '12:00')
b00.report(103, '12:00')
b00.report(104, '12:00')

b10.report(101, '12:15')
b10.report(102, '12:45')
b10.report(103, '12:45')
b10.report(104, '12:45')

b11.report(102, '12:30')
b11.report(103, '12:15')
b11.report(104, '12:15', '12:30')

b01.report(101, '12:45')
b01.report(102, '12:15')
b01.report(103, '12:30')

session.commit()
