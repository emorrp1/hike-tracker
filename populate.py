#!/usr/bin/python
from tracker import *

start()

b0 = Base(0,'000000')
b1 = Base(1,'000010')
b2 = Base(2,'010000')
b3 = Base(3,'010010')

save()

c = Route('clock', [0,1,3,2])
a = Route('anti', [0,2,3])

save()

Team(1, a)
Team(2, c)
Team(3, a)
Team(4, c)

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
