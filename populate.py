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

b0.report(101, '12:00', '12:00')
b0.report(102, '12:00', '12:00')
b0.report(103, '12:00', '12:00')
b0.report(104, '12:00', '12:00')

team_1.seen.append(br_noon_15)
team_2.seen.append(br_noon_45)
team_3.seen.append(br_noon_45)
team_4.seen.append(br_noon_45)

team_1.seen.append(tl_noon_45)

team_2.seen.append(tl_noon_15)
team_2.seen.append(tr_noon_30)

team_3.seen.append(tr_noon_15)
team_3.seen.append(tl_noon_30)

team_4.seen.append(tr_noon_15)
team_4.seen.append(tr_noon_30)

noon = datetime(2009,06,22,12,00)
noon_15 = datetime(2009,06,22,12,15)
noon_30 = datetime(2009,06,22,12,30)
noon_45 = datetime(2009,06,22,12,45)

br_noon = Event(time=noon,loc=br)
tr_noon = Event(time=noon,loc=tr)
tl_noon = Event(time=noon,loc=tl)
bl_noon = Event(time=noon,loc=bl)

br_noon_15 = Event(time=noon_15,loc=br)
tr_noon_15 = Event(time=noon_15,loc=tr)
tl_noon_15 = Event(time=noon_15,loc=tl)
bl_noon_15 = Event(time=noon_15,loc=bl)

br_noon_30 = Event(time=noon_30,loc=br)
tr_noon_30 = Event(time=noon_30,loc=tr)
tl_noon_30 = Event(time=noon_30,loc=tl)
bl_noon_30 = Event(time=noon_30,loc=bl)

br_noon_45 = Event(time=noon_45,loc=br)
tr_noon_45 = Event(time=noon_45,loc=tr)
tl_noon_45 = Event(time=noon_45,loc=tl)
bl_noon_45 = Event(time=noon_45,loc=bl)

