start('bf99.hike')

b00 = Base(00, '028683')
b21 = Base(21, '017671')
b22 = Base(22, '001660')
b23 = Base(23, '008646')
b24 = Base(24, '020647')
b25 = Base(25, '046653')
b26 = Base(26, '018685')
b27 = Base(27, '998685')
b28 = Base(28, '982672')
b29 = Base(29, '012663')
b30 = Base(30, '025656')
b31 = Base(31, '011708')
b99 = Base(99, '050660')

r1 = Route(1, [00,21,22,23,24,25,99])
r3 = Route(3, [00,26,27,28,22,29,30,99])
r5 = Route(5, [00,26,31,27,22,23,24,25,99])

t1 = Team(1, r5)
t2 = Team(2, r1)
t3 = Team(3, r5)
t4 = Team(4, r1)

Report(b00, 1, '12:00')
Report(b00, 2, '12:00')
Report(b00, 3, '12:00')
Report(b00, 4, '12:00')

Report(b21, 1, '12:45')
Report(b21, 2, '12:15')
Report(b21, 3, '12:30')

Report(b22, 1, '12:15')
Report(b22, 2, '12:45')
Report(b22, 3, '12:45')
Report(b22, 4, '12:45')

Report(b23, 2, '12:30')
Report(b23, 3, '12:15')
Report(b23, 4, '12:15', '12:30')

save()

