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

t1 = Team(number=1)
t2 = Team(number=2)
t3 = Team(number=3)
t4 = Team(number=4)

session.commit()

b00.report(1, '12:00')
b00.report(2, '12:00')
b00.report(3, '12:00')
b00.report(4, '12:00')

b10.report(1, '12:15')
b10.report(2, '12:45')
b10.report(3, '12:45')
b10.report(4, '12:45')

b11.report(2, '12:30')
b11.report(3, '12:15')
b11.report(4, '12:15', '12:30')

b01.report(1, '12:45')
b01.report(2, '12:15')
b01.report(3, '12:30')

session.commit()
