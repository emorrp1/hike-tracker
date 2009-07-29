#!/usr/bin/python
from tracker import *

start()

b0 = Base(0,'000000')
b1 = Base(1,'000010')
b2 = Base(2,'010000')
b3 = Base(3,'010010')

Team(1)
Team(2)
Team(3)
Team(4)

save()

b0.report(1, '12:00')
b0.report(2, '12:00')
b0.report(3, '12:00')
b0.report(4, '12:00')

b1.report(1, '12:45')
b1.report(2, '12:15')
b1.report(3, '12:30')

b2.report(1, '12:15')
b2.report(2, '12:45')
b2.report(3, '12:45')
b2.report(4, '12:45')

b3.report(2, '12:30')
b3.report(3, '12:15')
b3.report(4, '12:15', '12:30')

save()
