#!/usr/bin/python
from elixir import *
from model import *

metadata.bind = "sqlite:///custom.hike" # connect

setup_all()

Base(id=0,e=0,n=0)
Base(id=1,e=10,n=0)
Base(id=2,e=10,n=10)
Base(id=3,e=0,n=10)

Team(id=1)
Team(id=2)
Team(id=3)
Team(id=4)

session.commit()

Report(0, 1, '12:00')
Report(0, 2, '12:00')
Report(0, 3, '12:00')
Report(0, 4, '12:00')

Report(1, 1, '12:15')
Report(1, 2, '12:45')
Report(1, 3, '12:45')
Report(1, 4, '12:45')

Report(2, 2, '12:30')
Report(2, 3, '12:15')
Report(2, 4, '12:15', '12:30')

Report(3, 1, '12:45')
Report(3, 2, '12:15')
Report(3, 3, '12:30')

session.commit()
