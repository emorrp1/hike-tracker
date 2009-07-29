#!/usr/bin/python
from tracker import *

start()

b00 = Base(0,'000000')
b10 = Base(1,'010000')
b11 = Base(2,'010010')
b01 = Base(3,'000010')

Team(1)
Team(2)
Team(3)
Team(4)

save()

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

save()
