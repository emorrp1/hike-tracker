start()

b0 = Base('0', '000000')
b1 = Base('1', '000010')
b2 = Base('2', '010000')
b3 = Base('3', '010010')

r1 = Route('1', ['0','1','3','2'])
r2 = Route('2', ['0','2','3'])

t1 = Team('1', r2)
t2 = Team('2', r1)
t3 = Team('3', r2)
t4 = Team('4', r1)

Report(b0, '1', '12:00')
Report(b0, '2', '12:00')
Report(b0, '3', '12:00')
Report(b0, '4', '12:00')

Report(b1, '1', '12:45')
Report(b1, '2', '12:15')
Report(b1, '3', '12:30')

Report(b2, '1', '12:15')
Report(b2, '2', '12:45')
Report(b2, '3', '12:45')
Report(b2, '4', '12:45')

Report(b3, '2', '12:30')
Report(b3, '3', '12:15')
Report(b3, '4', '12:15', '12:30')

save()
