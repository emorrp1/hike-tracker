#!/usr/bin/python
from tracker import *

start()

Base(0,'000000')
Base(1,'010000')
Base(2,'010010')
Base(3,'000010')

Team(1)
Team(2)
Team(3)
Team(4)

save()

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

save()
